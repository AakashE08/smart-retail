# Smart Invoice Validation - Prototype

This directory contains the prototype deliverables for the **Smart Invoice Validation & Fraud Detection Platform**. It provides functional code elements and DevOps configuration suitable for a 2nd review presentation.

## Directory Structure
- `backend/` - Contains the Express.js based API handling invoice registration and QR-code-based verification workflows.
- `Jenkinsfile` - The proposed CI/CD pipeline definition as requested.
- `../Smart_Invoice_Validation_Platform_Report.md` - The detailed architecture & theoretical design project document.

## How to Run the Backend Prototype:

1. Ensure you have Node.js installed.
2. Navigate to the `backend/` directory using your terminal.
3. Run `npm install` to setup the Express framework and QR Code generation dependencies.
4. Run `npm start` to spin up the local application server.

### Demonstrating the Platform Applications:

**Application 1: Mimicking the Billing Software Plugin**
From your REST client (Postman/cURL), simulate a new invoice being generated:
- **POST** to `http://localhost:3000/api/invoice/register`
- **Payload:**
    ```json
    {
       "invoiceId": "INV-1002",
       "sellerGst": "29ABCDE1234F1Z5",
       "totalAmount": 1500,
       "gstAmount": 270,
       "products": ["Processor", "Motherboard"]
    }
    ```
The server will respond with a unique tracking ID and a Base-64 Data URI containing the generated QR Code to print on the physical bill.

**Application 2: Mimicking the Verification Scanner Algorithm**
Take the `verificationUrl` property returned by the previous request and put it into your browser or fire a `GET` request.
- **GET** `http://localhost:3000/api/invoice/verify/<INSERT-REFERENCE-NUMBER-HERE>`

The scanner will immediately report if the invoice is an authentic record matching the central database, or an invalid, potentially fraudulent fake.
