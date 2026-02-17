# Approach
### 1 - I used pdfplumber for text and table Extraction from PDFs.
### 2 - Configued table extraction with text-based horizontal/vertical strategies to handle table without explicit lines.
### 3 - I implemnet lightweight regex + spartial proximity to capture invoice data and totals into json format.

# Challenges
### 1 - Tables without grid lines strongly depend on text alignment and small layout changes break column detection.
### 2 - Complex invoices with multiple tables or wrapped text in cells can lead to merged/split columns.
### 3 - Field extraction via regex is sensitive to template variabtions

# Possible improvements
### 1 - Add template-specific configs (per client/vendor) with custom header regexes and column mappings
### 2 - Introduce an ml based table detector to robustly locate line items before text extraction
### 3 - Integrate OCR for scanned pdf or low quality images, then feed ocr output into the same talbe and field logic