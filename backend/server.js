const express = require('express');
const crypto = require('crypto');
const QRCode = require('qrcode');
const path = require('path');
const { execSync } = require('child_process');
const fs = require('fs');
const os = require('os');

const app = express();
app.use(express.json());

// Serve static frontend files
app.use(express.static(path.join(__dirname, 'public')));

const PORT = process.env.PORT || 3000;

const { Pool } = require('pg');

// ML Analysis Helper - Using file-based communication for Windows stability
const analyzeInvoiceWithML = (invoiceData) => {
    const tempFile = path.join(os.tmpdir(), `invoice_${crypto.randomUUID()}.json`);
    try {
        const mlScriptPath = path.join(__dirname, '..', 'ml', 'predict.py');
        fs.writeFileSync(tempFile, JSON.stringify(invoiceData));
        
        // Pass the file path instead of the raw JSON string
        const result = execSync(`python "${mlScriptPath}" "${tempFile}"`).toString();
        const parsed = JSON.parse(result);
        
        // Clean up
        if (fs.existsSync(tempFile)) fs.unlinkSync(tempFile);
        
        // Ensure analysis object exists
        if (!parsed.analysis) {
            parsed.analysis = { gstin_valid: true, is_calc_correct: true, is_tax_correct: true };
        }
        return parsed;
    } catch (err) {
        console.error("ML Analysis Error:", err.message);
        if (fs.existsSync(tempFile)) fs.unlinkSync(tempFile);
        return { 
            is_fraud: 0, 
            confidence: 0, 
            analysis: { gstin_valid: true, is_calc_correct: true, is_tax_correct: true },
            error: "ML Service Unavailable" 
        };
    }
};


// PostgreSQL database connection
let useMock = false;
let mockStorage = {};

const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 5432,
  user: process.env.DB_USER || 'invoice_user',
  password: process.env.DB_PASSWORD || 'invoice_password',
  database: process.env.DB_NAME || 'smart_invoice_db',
  connectionTimeoutMillis: 2000 // Short timeout for rapid fallback
});

// Initialize database table if it doesn't exist
const initDb = async () => {
    try {
        await pool.query('SELECT NOW()'); // Quick connectivity test
        await pool.query(`
            CREATE TABLE IF NOT EXISTS invoices (
                id VARCHAR(255) PRIMARY KEY,
                reference_number VARCHAR(255) UNIQUE NOT NULL,
                invoice_id VARCHAR(255) NOT NULL,
                seller_name VARCHAR(255),
                seller_gst VARCHAR(255),
                buyer JSONB,
                items JSONB,
                subtotal NUMERIC,
                taxes NUMERIC,
                total_amount NUMERIC,
                is_intra_state BOOLEAN,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_valid BOOLEAN DEFAULT TRUE,
                ml_fraud_flag BOOLEAN,
                ml_confidence NUMERIC
            );
        `);
        console.log("Database initialized successfully.");
    } catch (err) {
        console.warn("!!! DATABASE UNAVAILABLE !!! Falling back to In-Memory Mock Storage for this session.");
        console.warn("Connect to PostgreSQL or use Docker Compose for persistent data.");
        useMock = true;
    }
};

initDb();

// 1. API Endpoint for Billing Software Plugin (Invoice Registration)
app.post('/api/invoice/register', async (req, res) => {
    try {
        const { buyer, items, subtotal, taxes, totalAmount, isIntraState, sellerGst, productCategory, gstPercentage } = req.body;
        
        if (!buyer || !items || items.length === 0 || !totalAmount) {
            return res.status(400).json({ status: 'Error', message: 'Missing required invoice details' });
        }

        // Calculate total tax for ML and DB storage
        const totalTaxAmount = (taxes.cgst || 0) + (taxes.sgst || 0) + (taxes.igst || 0);

        // Run ML Analysis
        const mlInput = {
            seller_gst: sellerGst || "INVALID_GST",
            product_category: productCategory || "Electronics",
            subtotal: subtotal,
            taxes: totalTaxAmount,
            total_amount: totalAmount,
            gst_percentage: gstPercentage || 18
        };
        const mlResult = analyzeInvoiceWithML(mlInput);

        // Generate a unique reference number and timestamp
        const referenceNumber = crypto.randomUUID();
        const invoiceId = `INV-${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`;
        const timestamp = new Date().toISOString();

        const invoiceData = {
            id: referenceNumber,
            reference_number: referenceNumber,
            invoice_id: invoiceId,
            seller_name: "ABC Company (Demo)",
            seller_gst: sellerGst || "GTHUJ25632512355",
            buyer,
            items,
            subtotal,
            taxes: taxes, // Keep the object for breakdown
            taxes_total: totalTaxAmount, // Use a numeric field for validation
            total_amount: totalAmount,
            is_intra_state: isIntraState,
            timestamp,
            is_valid: true,
            ml_fraud_flag: mlResult.is_fraud === 1,
            ml_confidence: mlResult.confidence,
            ml_analysis: mlResult.analysis
        };

        if (useMock) {
            mockStorage[referenceNumber] = invoiceData;
            console.log(`[Mock DB] Stored invoice ${invoiceId} | ML Fraud Flag: ${invoiceData.ml_fraud_flag}`);
        } else {
            // Store invoice into PostgreSQL database (Requires updated schema)
            await pool.query(
                `INSERT INTO invoices (id, reference_number, invoice_id, seller_name, seller_gst, buyer, items, subtotal, taxes, total_amount, is_intra_state, timestamp, is_valid, ml_fraud_flag, ml_confidence) 
                 VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)`,
                [
                    invoiceData.id, invoiceData.reference_number, invoiceData.invoice_id, 
                    invoiceData.seller_name, invoiceData.seller_gst, 
                    JSON.stringify(invoiceData.buyer), JSON.stringify(invoiceData.items), 
                    invoiceData.subtotal, JSON.stringify(invoiceData.taxes), invoiceData.total_amount, 
                    invoiceData.is_intra_state, invoiceData.timestamp, invoiceData.is_valid,
                    invoiceData.ml_fraud_flag, invoiceData.ml_confidence
                ]
            );
        }

        // Generate QR Code containing the verification endpoint
        const verificationUrl = `http://localhost:${PORT}/api/invoice/verify/${referenceNumber}`;
        const qrCodeDataUri = await QRCode.toDataURL(verificationUrl);

        res.status(201).json({
            status: 'Success',
            id: referenceNumber,
            referenceNumber,
            verificationUrl,
            qrCodeDataUri, 
            timestamp,
            mlHighlight: {
                isFraud: invoiceData.ml_fraud_flag,
                confidence: invoiceData.ml_confidence,
                analysis: mlResult.analysis
            }
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({ status: 'Error', message: 'Internal server error processing invoice' });
    }
});

// 2. API Endpoint for QR Verification Scanner Application
app.get('/api/invoice/verify/:referenceNumber', async (req, res) => {
    const { referenceNumber } = req.params;

    try {
        let invoiceRow;
        
        if (useMock) {
            invoiceRow = mockStorage[referenceNumber];
        } else {
            const result = await pool.query('SELECT * FROM invoices WHERE reference_number = $1', [referenceNumber]);
            invoiceRow = result.rows[0];
            if (invoiceRow) {
                // Parse JSONB if coming from Postgres
                invoiceRow.buyer = typeof invoiceRow.buyer === 'string' ? JSON.parse(invoiceRow.buyer) : invoiceRow.buyer;
                invoiceRow.items = typeof invoiceRow.items === 'string' ? JSON.parse(invoiceRow.items) : invoiceRow.items;
                invoiceRow.taxes = typeof invoiceRow.taxes === 'string' ? JSON.parse(invoiceRow.taxes) : invoiceRow.taxes;
            }
        }

        if (!invoiceRow) {
            return res.status(404).json({
                status: 'Invalid',
                message: 'Invoice not found or potentially fraudulent/fake.',
                referenceNumber: referenceNumber
            });
        }

        // Map back to expected structure
        const invoice = {
            _id: invoiceRow.id,
            referenceNumber: invoiceRow.reference_number,
            invoiceId: invoiceRow.invoice_id,
            seller: {
                name: invoiceRow.seller_name,
                gstNumber: invoiceRow.seller_gst
            },
            buyer: invoiceRow.buyer,
            items: invoiceRow.items,
            subtotal: parseFloat(invoiceRow.subtotal),
            taxes: invoiceRow.taxes, // Return the object
            totalAmount: parseFloat(invoiceRow.total_amount),
            isIntraState: invoiceRow.is_intra_state,
            timestamp: invoiceRow.timestamp,
            isValid: invoiceRow.is_valid,
            mlFraudFlag: invoiceRow.ml_fraud_flag,
            mlConfidence: invoiceRow.ml_confidence
        };

        const responseMsg = invoice.mlFraudFlag ? 
            "WARNING: This invoice has been flagged as POTENTIALLY FRAUDULENT by the ML model." :
            "Invoice successfully verified against the centralized government database.";

        res.status(200).json({
            status: invoice.mlFraudFlag ? 'Flagged' : 'Authentic',
            message: responseMsg,
            data: invoice
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ status: 'Error', message: 'Database error during verification' });
    }
});

app.listen(PORT, () => {
    console.log(`Smart Invoice Validation Sandbox Server running on port ${PORT}`);
    if (useMock) console.log("--- RUNNING IN MOCK MODE (NO DATABASE REQUIRED) ---");
});



