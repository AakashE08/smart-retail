# PowerShell Script to perfectly mock a Jenkins Pipeline Output
$host.UI.RawUI.WindowTitle = "Jenkins Automation - Jenkins CI"

Function Print-Colored {
    param([string]$text, [string]$color="White")
    Write-Host $text -ForegroundColor $color
}

Function Print-Step {
    param([string]$stepName)
    Write-Host "[Pipeline] " -ForegroundColor DarkGray -NoNewline
    Write-Host "stage" -ForegroundColor Cyan
    Write-Host "[Pipeline] { ($stepName)" -ForegroundColor DarkGray
}

Function Print-Step-End {
    Write-Host "[Pipeline] }" -ForegroundColor DarkGray
}

Clear-Host
Write-Host "Started by user bobby"
Write-Host "Running in Durability level: MAX_SURVIVABILITY"
Write-Host "[Pipeline] Start of Pipeline" -ForegroundColor DarkGray
Write-Host "[Pipeline] node" -ForegroundColor DarkGray
Write-Host "Running on Jenkins in C:\Jenkins\workspace\smart-invoice-platform"

# ------- STAGE 1
Print-Step "Source Control Management (Git + GitHub)"
Start-Sleep -Seconds 1
Print-Colored " > git rev-parse --resolve-git-dir C:\Jenkins\workspace\smart-invoice-platform\.git # timeout=10" "Gray"
Print-Colored "Fetching changes from the remote Git repository (GitHub)..." "Gray"
Print-Colored " > git config remote.origin.url https://github.com/organization/smart-invoice-platform.git # timeout=10" "Gray"
Print-Colored "Checking out Revision 8a9b2c3d4e5f6g7h8i9j0 (refs/remotes/origin/main)" "Gray"
Print-Colored "Commit message: `"feat: Include PostgreSQL integration & Dockerization`"" "Gray"
Print-Step-End

# ------- STAGE 2
Print-Step "Backend Setup (Node.js + Express.js)"
Start-Sleep -Seconds 2
Print-Colored "[smart-invoice-platform] $ npm install --omit=dev" "Gray"
Print-Colored "added 114 packages, and audited 115 packages in 3s" "White"
Print-Colored "found 0 vulnerabilities" "Green"
Print-Step-End

# ------- STAGE 3
Print-Step "Database Update (PostgreSQL)"
Start-Sleep -Seconds 2
Print-Colored "[smart-invoice-platform] $ npm run migrate:postgres" "Gray"
Print-Colored "Connecting to PostgreSQL database..." "White"
Print-Colored "Applying schema '001_invoice_records.sql'..." "Gray"
Print-Colored "Applying schema '002_verification_logs.sql'..." "Gray"
Print-Colored "Successfully migrated PostgreSQL schema to latest version." "Green"
Print-Step-End

# ------- STAGE 4
Print-Step "Run Unit & API Tests"
Start-Sleep -Seconds 2
Print-Colored "[smart-invoice-platform] $ npm test" "Gray"
Write-Host ""
Print-Colored "  Smart Invoice API Tests" "White"
Start-Sleep -Milliseconds 500
Print-Colored "    √ should generate unique reference ID on register (45ms)" "Green"
Start-Sleep -Milliseconds 400
Print-Colored "    √ should return 400 if invoice details are missing (12ms)" "Green"
Start-Sleep -Milliseconds 500
Print-Colored "    √ should generate valid QR payload (80ms)" "Green"
Start-Sleep -Milliseconds 300
Print-Colored "    √ should verify authentic invoice and return 200 OK (22ms)" "Green"
Start-Sleep -Milliseconds 600
Print-Colored "    √ check postgres lookup for duplicate submissions (110ms)" "Green"
Start-Sleep -Milliseconds 500
Print-Colored "    √ should return 404 for invalid forged invoice QR ref (18ms)" "Green"
Write-Host ""
Print-Colored "  6 passing (287ms)" "Green"
Print-Step-End

# ------- STAGE 5
Print-Step "Containerization (Docker)"
Start-Sleep -Seconds 2
Print-Colored "[smart-invoice-platform] $ docker build -t scm/smart-invoice-backend:v1.2.0 ." "Gray"
Start-Sleep -Seconds 1
Print-Colored "Sending build context to Docker daemon  45.5MB" "White"
Print-Colored "Step 1/6 : FROM node:18-alpine" "White"
Print-Colored " ---> 4a4f8d9c2e1b" "White"
Print-Colored "Step 2/6 : WORKDIR /usr/src/app" "White"
Start-Sleep -Milliseconds 500
Print-Colored " ---> Running in 8b7c6d5e4f3a" "White"
Print-Colored "Step 3/6 : COPY package*.json ./" "White"
Start-Sleep -Milliseconds 500
Print-Colored " ---> 1a2b3c4d5e6f" "White"
Print-Colored "Step 4/6 : RUN npm install --production" "White"
Start-Sleep -Seconds 1
Print-Colored " ---> 9f8e7d6c5b4a" "White"
Print-Colored "Step 5/6 : COPY . ." "White"
Print-Colored "Step 6/6 : EXPOSE 3000" "White"
Print-Colored "Successfully built 2b4d6f8a0c1e" "Green"
Print-Colored "Successfully tagged scm/smart-invoice-backend:v1.2.0" "Green"
Print-Step-End

# ------- STAGE 6
Print-Step "Deploy to Pipeline CI/CD Server"
Start-Sleep -Seconds 2
Print-Colored "[smart-invoice-platform] $ kubectl apply -f k8s/deployment.yaml" "Gray"
Print-Colored "deployment.apps/smart-invoice-backend configured" "White"
Print-Colored "service/smart-invoice-service unchanged" "White"
Print-Colored "[smart-invoice-platform] $ kubectl rollout status deployment/smart-invoice-backend" "Gray"
Start-Sleep -Seconds 2
Print-Colored "Waiting for deployment `"smart-invoice-backend`" rollout to finish: 1 out of 3 new replicas have been updated..." "White"
Start-Sleep -Seconds 2
Print-Colored "Waiting for deployment `"smart-invoice-backend`" rollout to finish: 2 out of 3 new replicas have been updated..." "White"
Start-Sleep -Seconds 2
Print-Colored "deployment `"smart-invoice-backend`" successfully rolled out" "Green"
Print-Step-End

Write-Host "[Pipeline] End of Pipeline" -ForegroundColor DarkGray
Write-Host "Finished: SUCCESS" -ForegroundColor Green
Write-Host ""
Write-Host -NoNewline "Pipeline simulation completed. " -ForegroundColor Yellow
Write-Host "Code successfully deployed!" -ForegroundColor Green
