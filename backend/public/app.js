document.addEventListener('DOMContentLoaded', () => {
    
    // --- Application 1: Billing Form Submission --- 
    const generateForm = document.getElementById('generateForm');
    const generationResult = document.getElementById('generationResult');
    
    generateForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Build Data Payload mapping the Next.js `create-bill-form.tsx` schema
        const buyer = {
            name: document.getElementById('buyerName').value,
            gstNumber: document.getElementById('buyerGst').value,
            address: document.getElementById('buyerAddress').value,
            state: document.getElementById('buyerState').value,
            stateCode: document.getElementById('buyerStateCode').value
        };

        const sellerGst = document.getElementById('sellerGst').value;
        const productCategory = document.getElementById('productCategory').value;
        const gstPct = parseFloat(document.getElementById('itemGst').value) || 0;
        const qty = parseFloat(document.getElementById('itemQty').value) || 0;
        const rate = parseFloat(document.getElementById('itemRate').value) || 0;

        const items = [{
            name: document.getElementById('itemName').value,
            hsnCode: "1234",
            quantity: qty,
            rate: rate,
            gstPercentage: gstPct
        }];

        // Calculations replicating Next.js logic
        const subtotal = qty * rate;
        const taxAmount = (subtotal * gstPct) / 100;
        
        // Demo logic: If State Code is 29 (Karnataka), it's IntraState (CGST + SGST). Else IGST.
        const isIntraState = buyer.stateCode === "29";
        const taxes = { cgst: 0, sgst: 0, igst: 0 };
        
        if (isIntraState) {
            taxes.cgst = taxAmount / 2;
            taxes.sgst = taxAmount / 2;
        } else {
            taxes.igst = taxAmount;
        }
        
        const totalAmount = subtotal + taxes.cgst + taxes.sgst + taxes.igst;

        try {
            const response = await fetch('/api/invoice/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    buyer, items, subtotal, taxes, totalAmount, isIntraState,
                    sellerGst, productCategory, gstPercentage: gstPct
                })
            });

            const data = await response.json();
            
            if (response.ok) {
                // Display result
                document.getElementById('resRefId').innerText = data.referenceNumber;
                document.getElementById('resTimestamp').innerText = new Date(data.timestamp).toLocaleString();
                document.getElementById('resQrCode').src = data.qrCodeDataUri;
                
                // ML Highlights
                const mlRes = data.mlHighlight || { isFraud: false, confidence: 0, analysis: {} };
                const mlInsight = document.getElementById('mlRegInsight');
                const mlContent = document.getElementById('mlRegContent');
                
                const analysis = mlRes.analysis || { gstin_valid: true, is_calc_correct: true, is_tax_correct: true };
                
                mlInsight.classList.remove('hidden');
                const statusBadge = mlRes.isFraud ? 
                    '<span class="ml-badge ml-badge-danger">FLAGGED</span>' : 
                    '<span class="ml-badge ml-badge-success">SECURE</span>';
                
                mlContent.innerHTML = `
                    <p>${statusBadge} ML model analyzed the invoice creation patterns.</p>
                    <ul style="padding-left: 1.25rem; margin-top: 0.5rem;">
                        <li>GSTIN Format: ${analysis.gstin_valid ? '✅ Valid' : '❌ Invalid Pattern'}</li>
                        <li>Calculation Check: ${analysis.is_calc_correct ? '✅ Verified' : '❌ Mismatch Found'}</li>
                        <li>Tax Code Audit: ${analysis.is_tax_correct ? '✅ Matches Category' : '❌ Rate Irregularity'}</li>
                    </ul>
                `;


                generationResult.classList.remove('hidden');
            } else {
                alert('Generation Failed: ' + data.message);
            }
        } catch (err) {
            console.error(err);
            alert('Error connecting to server.');
        }
    });

    // Copy reference ID convenience
    document.getElementById('copyRefBtn').addEventListener('click', () => {
        const refId = document.getElementById('resRefId').innerText;
        navigator.clipboard.writeText(refId);
        const scanInput = document.getElementById('scanRefId');
        scanInput.value = refId;
        
        // Visual feedback
        const btn = document.getElementById('copyRefBtn');
        btn.innerText = "Copied & Pasted!";
        setTimeout(() => btn.innerText = "Copy Reference ID", 2000);
    });


    // --- Application 2: Verification Scanner ---
    const verifyForm = document.getElementById('verifyForm');
    const verificationResult = document.getElementById('verificationResult');
    
    verifyForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const refId = document.getElementById('scanRefId').value.trim();
        if(!refId) return;

        try {
            const response = await fetch(`/api/invoice/verify/${refId}`);
            const data = await response.json();
            
            verificationResult.classList.remove('hidden');
            const statusBanner = document.getElementById('statusBanner');
            const detailsDiv = document.getElementById('invoiceDetails');
            const mlInsight = document.getElementById('mlVerifyInsight');
            const mlContent = document.getElementById('mlVerifyContent');
            
            if (response.ok) {
                // Authentic Invoice matched
                const inv = data.data;
                
                statusBanner.className = 'status-banner ' + (inv.mlFraudFlag ? 'status-error' : 'status-success');
                statusBanner.innerHTML = inv.mlFraudFlag ? 'ALERT: Authentic Record but Flagged for Fraud' : 'VALID: Authentic Govt. Record';
                
                // Show ML Insights
                mlInsight.classList.remove('hidden');
                mlContent.innerHTML = `
                    <p>${inv.mlFraudFlag ? '🚨 High probability of fraud detected.' : '✅ No anomalies detected in this bill record.'}</p>
                    <p style="font-size: 0.75rem; margin-top: 0.5rem; color: #6b7280;">
                        Analysis Confidence: ${(inv.mlConfidence * 100).toFixed(1)}%
                    </p>
                `;

                detailsDiv.innerHTML = `
                    <div style="font-weight:600; font-size: 1rem; margin-bottom: 1rem;">Invoice #${inv.invoiceId}</div>
                    
                    <div class="detail-row">
                        <span class="detail-label">Seller GSTIN</span>
                        <span class="detail-value">${inv.seller.gstNumber}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Customer Name</span>
                        <span class="detail-value">${inv.buyer.name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Buyer GSTIN</span>
                        <span class="detail-value">${inv.buyer.gstNumber}</span>
                    </div>
                    
                    <div class="totals-section">
                        <div class="totals-row">
                            <span>Subtotal</span>
                            <span>₹${inv.subtotal.toLocaleString("en-IN")}</span>
                        </div>
                        ${inv.isIntraState ? `
                        <div class="totals-row">
                            <span>CGST + SGST</span>
                            <span>₹${inv.taxes.cgst.toLocaleString("en-IN", {maximumFractionDigits:2})} + ₹${inv.taxes.sgst.toLocaleString("en-IN", {maximumFractionDigits:2})}</span>
                        </div>` : `
                        <div class="totals-row">
                            <span>IGST</span>
                            <span>₹${inv.taxes.igst.toLocaleString("en-IN", {maximumFractionDigits:2})}</span>
                        </div>`}
                        <div class="totals-row bold">
                            <span>Total Amount</span>
                            <span>₹${inv.totalAmount.toLocaleString("en-IN", {maximumFractionDigits:2})}</span>
                        </div>
                    </div>
                `;
            } else {
                // Fraud/Invalid
                statusBanner.className = 'status-banner status-error';
                statusBanner.innerHTML = 'ALERT: Unregistered / Fake Reference ID';
                mlInsight.classList.add('hidden');
                
                detailsDiv.innerHTML = `
                    <div class="detail-row">
                        <span class="detail-label">Scanned Ref</span>
                        <span class="detail-value monospaced">${refId}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Error</span>
                        <span class="detail-value">No DB record found</span>
                    </div>
                `;
            }

        } catch (err) {
            console.error(err);
            alert('Error connecting to verification server.');
        }
    });
});

