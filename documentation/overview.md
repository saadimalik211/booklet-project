# Lavaro Group – Booklet PDF Maker (Modernized Documentation)

## Overview
The Booklet PDF Maker is a system for generating structured PDF “Books” that contain ordered sets of “Pages.” Each book is tailored to a specific customer, using customer attributes and optionally user-uploaded spreadsheets.  

The system allows dynamic customization of pages based on customer data and supports multiple file types including static PDFs, fillable PDFs, and Excel spreadsheets.

---

## Entities

### **Books**
- A **Book** is a collection of ordered **Pages**.
- Users can define different types of books (e.g., **Renewal Book**, **Employee Benefits Book**).
- Each book specifies the sequence of pages and how they are generated.

---

### **Pages**
Pages are the components of a book. Each page can be one of the following types:

1. **Static Page**  
   - Fixed content page.  
   - Example: “About the Company.”

2. **PDF Form (Plain)**  
   - A PDF file used directly as a page.

3. **PDF Form (Fillable)**  
   - A PDF template with fields that can be filled in with data.

4. **Choosable Static Page**  
   - A conditional page that uses **Customer Attributes** to determine which PDF is included.  
   - Example: Selecting a specific **Sales Representative**’s PDF page.

5. **Microsoft Excel Document Page**  
   - A page generated from a specific worksheet tab in an uploaded Excel file.  
   - Represented as a page in the book.  
   - Requires the user to upload a spreadsheet with correct tab names.

---

### **Customer**
- Customers are stored in the system.  
- Each customer has attributes stored with them.  
- Attributes are grouped by **Year + Quarter** (for versioning).  
- A user can fill in or update customer attributes.

---

### **Customer Attribute**
- Stored as **Key → Value** pairs.  
- Unlimited attributes per customer.  
- Attributes drive conditional page selection.  

#### Example Attributes
- `Medical_Plan_Company_Name`
- `Address`
- `Logo`
- `Sales_Representative`

---

## Example Workflow

### **Book Definition**
A user defines a **Renewal Book** with the following pages:
1. **Static Page** → Cover page.  
2. **Static Page** → Company information.  
3. **Choosable Static Page** → Uses the customer’s `Sales_Representative` attribute:
   - If `Sales_Representative = A` → Insert Page X  
   - If `Sales_Representative = B` → Insert Page Y  
4. **Microsoft Excel Document Page** → Uses uploaded spreadsheet, tab `"DBL PROPOSAL"`  

---

### **Book Generation**
When generating a book:
1. User selects a **Customer**.  
2. User selects a **Book** to generate.  
3. If the book includes Excel-based pages, the user must upload the required spreadsheet.  

#### Example Output
- **Page 1** → Static cover page.  
- **Page 2** → Static company info.  
- **Page 3** → Based on `Sales_Representative` attribute, choose correct page.  
- **Page 4** → Extract `"DBL PROPOSAL"` worksheet from uploaded spreadsheet and render as PDF page.  

---

## Implementation Stack (Python)
- **API**: FastAPI
- **Worker**: Celery + Redis/RabbitMQ
- **PDF**: PyPDF2 + ReportLab (+ borb/pdfrw optional)
- **Excel**: openpyxl (+ pandas optional)
- **DB/ORM**: PostgreSQL + SQLAlchemy (+ Alembic)
- **Auth**: OAuth2 + JWT
- **HTML→PDF (optional)**: WeasyPrint


