# **AI Financial Reviewer – Product Requirements Document (PRD)**

## **1  Overview**

The **AI Financial Reviewer** is an intelligent agent that automates extraction, transformation and analysis of personal‑finance data that currently lives in disparate PDFs, CSVs and screenshots.  
 Phase 1 (MVP) keeps Google Sheets as the system of record while eliminating manual copy‑paste and formula maintenance.

---

## **2  Goals**

| Horizon | Goal |
| ----- | ----- |
| **MVP (now)** | • Allow a user to **upload statements via a simple web UI**.• Parse Monzo CSV (budget), Chip PDF (savings) and Vanguard PNG (investments).• Normalise records into a common schema.• Append cleaned rows into three existing Google‑Sheet tabs:  • **Portfolio Transactions**   • **Budget Transactions** (raw)  • **Budget Transaction Tagging** (formula‑driven view) |
| **H2 (next)** | Migrate storage from Google Sheets to a relational/columnar DB and auto‑generate dashboards **and natural‑language querying**. |
| **H3 (later)** | Direct account integrations (OAuth / web‑scraping) for real‑time ingestion; conversational insights; mobile app. |

*Note – NL querying is **explicitly out of scope for the MVP** and will begin in H2.*

---

## **3  Key Feature Map**

1. **Upload UI** *(MVP, new)*  
    • Drag‑and‑drop zone \+ “Browse files…” button.  
    • Accept multiple files (PDF, CSV, PNG/JPG).  
    • Inline validation (size ≤ 10 MB, allowed mime‑types).  
    • Live list showing *Filename • Detected Type • Target Sheet • Status (Queued ▸ Processing ▸ Done / Error)*.  
    • Optional drop‑down to override auto‑routing (e.g. force a PDF into Budget sheet).  
    • **Preview of extracted rows before final confirmation**.  
    • Progress bar & toast notifications.  
    • Auth: Google Sign‑in (OAuth) so the app can write to the user’s sheet.

2. **Extraction Pipeline**  
    • `extract_pdf(pdf)`, `extract_csv(csv)`, `extract_image(img)` wrappers.  
    • Use LLM‑OCR (e.g. GPT‑4o Vision) for images; pdfplumber / Camelot for PDFs; pandas for CSV.  
    • Return list ⟨dict⟩ in **Raw Record** schema.

3. **Transformation Layer**  
    • Portfolio & Image/PDF sources → apply schema mapping only (the sheet’s own formulas will populate **Transaction Type** and **Order Value**).  
    • **Budget CSV uploads → *no transformation***; columns are copied 1‑to‑1 into the **Budget Transactions** tab with a single extra column **Tag** (user‑selectable: Fola | Pippa).  
    • Deduplicate by hashing relevant columns and **flag duplicates** (no overwrite).

4. **Google Sheets Writer**  
    • `append_rows(sheet_id, tab_id, rows)` with exponential back‑off.  
    • Keeps header row locked; inserts below last‑filled row.  
    • After inserting into **Budget Transactions**, *auto‑extend formulas* in the downstream **Budget Transaction Tagging** sheet by **filling the last formula row downward to cover new rows** (simulates user drag‑fill).  
    • Confirm formula propagation by ensuring that **all formula‑driven columns (e.g., Date, Name)** return a value for each new row — or, at minimum, that the total row count in **Budget Transaction Tagging** matches the **Budget Transactions** sheet after the fill operation.  
    • **LLM category suggestion**: after formula propagation, automatically detect rows where `Retag` is blank and prompt the LLM with that row’s *Notes & \#tags* (and, if helpful, *Name*) together with the category list from **Category Definitions**. The agent writes the result into a new column **Retag Suggested (LLM)** (or directly into `Retag` if we adopt auto‑fill).

5. **(Out‑of‑scope for MVP)** Dashboards, NLQ, database storage, direct platform integrations.

---

## **4  Data Schemas**

### **4.1  Portfolio Transactions**

| Column | Description |
| ----- | ----- |
| Asset | {Cash, Crypto, Stocks, Private Stocks, ETF, Pensions, Bonds} |
| Ticker | Ticker for Crypto/Stocks only |
| Platform | Source platform (e.g. Vanguard) |
| Description | Friendly name of asset/product |
| Transaction Date | DD/MM/YYYY |
| Units | \+ve buy / –ve sell / 0 (meta) |
| Transaction Type | **Sheet formula (`=IF(Units>0,"Buy","Sell")`); agent leaves blank** |
| Transaction Price | £ price per unit (Cash=£1) |
| Order Value | **Sheet formula (`=Units×Price`, e.g. `=F*H`); agent leaves blank** |
| Tax / Fees | Fees/taxes paid |
| Cum. Interest / Dividends | Earnings since previous record |
| Tag | {Fola, Pippa, Ileri, Tami} |

*Asset‑specific rules*  
 • **Cash**: Price=1; interest‑only rows→Units 0 \+ Cum.Interest set.  
 • **ETF**: Fee‑only rows→Units 0 \+ Tax/Fee set.

### **4.2  Budget Transactions (Raw CSV → Sheet gid `1640613480`)**

Full one‑to‑one dump of Monzo export **plus** an extra **Tag** column.

| Column (Monzo order) | Sample Mapping |
| ----- | ----- |
| Transaction ID | A |
| Date | B |
| Time | C |
| Type | D |
| Name | E |
| Emoji | F |
| Category | G |
| Amount | H |
| Currency | I |
| Local Amount | J |
| Local Currency | K |
| Notes & \#tags | L |
| Address | M |
| Receipt | N |
| Description | O |
| Category Split | P |
| Money Out | Q |
| Money In | R |
| **Tag (new)** | S |

*Only the **Tag** column is writable by the agent; all other data is verbatim from CSV.*

### **4.3  Budget Transaction Tagging (Sheet gid `741116542 – formula view`)**

Formula‑driven sheet that enriches/retags Budget data. The agent **never edits formulas**; it only propagates them downward after new rows are added in §4.2. Key columns:

| Column | Formula Template |
| ----- | ----- |
| Transaction ID | `='Budget Transactions'!A{row}` |
| Date | `=INDEX('Budget Transactions'!B$2:B, MATCH($A{row}, 'Budget Transactions'!$A$2:$A, 0))` |
| … | … |
| Retag | `=INDEX('Category Definitions'!$B$27:$B, MATCH($F{row}, 'Category Definitions'!$A$27:$A, 0))` |
| **Retag Suggested (LLM)** | Filled only when **Retag** is blank; agent‑generated category suggestion based on Notes/\#tags & category mapping |
| Tag | `=INDEX('Budget Transactions'!S$2:S, MATCH($A{row}, 'Budget Transactions'!$A$2:$A, 0))` |

Category rules are defined in **Category Definitions** sheet (gid `1930933053`).

---

## **5  UX Requirements (Upload UI)**

| ID | Requirement | Priority |
| ----- | ----- | ----- |
| **UI‑1** | The landing page shows a file‑upload card with drag‑and‑drop and a "Browse" button. | P0 |
| **UI‑2** | After files are selected, each appears in a table with Type icon, detected target (Portfolio/Budget), and a status badge. | P0 |
| **UI‑3** | While processing, show an animated progress indicator. | P0 |
| **UI‑4** | On success, show green "Done" and row count appended; on failure, show red "Error" with tooltip. | P0 |
| **UI‑5** | User can manually override the target sheet before upload completes. | P1 |
| **UI‑6** | Responsive design (desktop & mobile). | P1 |
| **UI‑7** | Brand‑neutral light theme using TailwindCSS. | P2 |
| **UI‑8** | **Preview the extracted rows and allow the user to confirm/abort before writing to Sheets.** | P1 |

---

## **6  Non‑Functional Requirements**

* **Security**: OAuth‑2 with least‑privilege Google Sheets scope; encrypt tokens at rest.

* **Perf**: End‑to‑end upload→sheet append in \< 10 s for ≤ 200 rows.

* **Scalability**: Pipeline functions stateless; ready for serverless deployment (Cloud Functions).

* **Observability**: Structured logs (JSON); error tracking via Sentry.

---

## **7  Suggested Tech Stack (MVP)**

| Layer | Tech |
| ----- | ----- |
| Frontend | Streamlit (Python) \+ streamlit‑dropzone component |
| Backend | FastAPI (Python 3.12) |
| LLM/OCR | OpenAI GPT‑4o Vision (image & pdf fallback) |
| Storage | Google Sheets (gspread) |
| Auth | Google OAuth 2.0 |
| Deployment | Cloud Run / Fly.io |

---

## **8  Decisions & Remaining Questions**

| \# | Topic | Decision / Status |
| ----- | ----- | ----- |
| 1 | **Canonical Sheets & Tabs** | Spreadsheet ID: `1L8VgK5DIKqaU5VzGeqLHVMhrMEbZ28RfiXn_y95bgC4`.• Portfolio Transactions → gid `823039374`  Budget Transactions (raw) → gid `1640613480` Budget Transaction Tagging → gid `741116542` (auto‑fill formulas) |
| 2 | **Duplicate handling** | **Flag** duplicates in the UI/logs (do not overwrite or silently skip). |
| 3 | **Supported file types** | **Images (PNG/JPG), CSV, PDF** only. |
| 4 | **Category Mapping Source** | Sheet “Category Definitions” gid `1930933053`. |

---

## **9  Risks & Mitigations**

| Risk | Mitigation |
| ----- | ----- |
| OCR mis‑reads low‑quality screenshots (Vanguard) | Set min‑resolution guidance; allow user preview & edit (UI‑8); log confidence scores. |
| PDF table structure variability (Chip) | Use dual strategy: tabula/Camelot first, fall back to GPT‑4o Vision table extraction. |
| Formula propagation to Tagging sheet fails | Validate row count post‑write; re‑apply fill if mismatch; alert on error. |
| Growing sheet row‑count slows API calls | Batch appends (500 rows/call) and advise DB migration in H2. |
| User uploads duplicate files | Compute file hash \+ dedup hash key at transform layer; surface duplicate flag. |

---

## **10  Milestones & Timeline (T‑shirt sizing)**

| Week | Deliverable |
| ----- | ----- |
| 1 | FE upload widget & Google OAuth wiring |
| 2 | CSV extractor & raw Budget write path |
| 3 | PDF extractor & Portfolio write path |
| 4 | Image OCR extractor \+ Preview component |
| 5 | Tagging sheet formula‑propagation logic \+ unit tests |
| 6 | Beta test with real statements \+ bug‑fixes |

---

### **End of Document**

