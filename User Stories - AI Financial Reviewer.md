# **AI Financial Reviewer – One‑Story‑Point Backlog**

---

## **Legend**

1. **Priority**: P0 = Must‑have, P1 = Should‑have (WSJF / RICE blended).  
2. All stories are **1 SP** (≤ 1 dev‑day) and satisfy **INVEST**.  
3. **Dependencies** are limited to direct prerequisites.

---

## **Epic 1 – Authentication & Authorization**

| ID | User Story | Acceptance Criteria | Priority | Dependencies |
| ----- | ----- | ----- | ----- | ----- |
| **US‑A1** | *As an unauthenticated visitor, I want to sign in with Google so that the app can securely access my Sheets.* | ▸ **Given** I'm on the landing page, **when** I click **“Sign in with Google”**, **then** I'm redirected to the Google OAuth consent screen. ▸ **Given** I grant consent, **when** the OAuth flow completes, **then** the app receives **access & refresh tokens** and my avatar appears in the nav bar. ▸ **Given** an expired token, **when** I make a request, **then** the system transparently **refreshes** the token and retries once. | P0 | — |
| **US‑A2** | *As a developer, I want the backend to verify Google ID tokens so that only authenticated calls succeed.* | ▸ **Given** a request with a valid token, **when** verification passes, **then** the API proceeds and returns 200\. ▸ **Given** a request with an invalid/expired token, **when** verification fails, **then** the API returns 401 and a JSON error body. ▸ **Given** repeated 401s for the same user, **when** threshold \> 3, **then** a warning is logged to Sentry. | P0 | US‑A1 |
| **US‑A3** | *As a user, I want the OAuth flow to request least‑privilege scopes so that my privacy is protected.* | ▸ **Given** the consent screen, **when** scopes display, **then** only the **Google Sheets** scope is requested. ▸ **Given** I deny permission, **when** control returns, **then** a blocking error with a **retry** option is shown. ▸ **Given** permission granted, **when** a smoke test runs, **then** the app successfully reads my spreadsheet metadata. | P0 | US‑A1 |
| **US‑A4** | *As a system, I want to securely store OAuth tokens so that users don’t need to re‑authenticate every visit.* | Given a user authenticates, when tokens are received, then they’re AES‑256‑encrypted at rest.  Given encrypted tokens exist, when the user returns within 30 days, then they’re automatically authenticated via refresh token. Given stored tokens are invalid, when the API call fails, then the user is redirected to re‑authenticate. | P0 | US‑A1 |

---

## **Epic 2 – Upload UI**

| ID | User Story | Acceptance Criteria | Priority | Dependencies |
| ----- | ----- | ----- | ----- | ----- |
| **US‑U1** | *As a signed‑in user, I want a drag‑and‑drop zone & “Browse” button so that I can add files quickly.* | ▸ **Given** the dashboard, **when** the page loads, **then** a drop‑zone with copy *“Drop CSV/PDF/PNG here or Browse”* is visible. ▸ **Given** I drop ≤ 10 MB files, **when** they enter the zone, **then** rows appear in the queue table with status **Queued**. ▸ **Given** I click **Browse**, **when** file‑picker opens, **then** it filters to *.csv, .pdf, .png, .jpg*. | P0 | US‑A1 |
| **US‑U2** | *As a user, I want client‑side validation of size & mime‑type so that invalid files are blocked early.* | ▸ **Given** a \> 10 MB file, **when** I attempt to upload, **then** an error toast *“File exceeds 10 MB limit”* is shown and file is rejected. ▸ **Given** file selected, **when** type not CSV/PDF/PNG/JPG, **then** an *invalid type* toast appears. ▸ **Given** valid files, **when** selected, **then** no validation errors fire. **Given** valid file, **when** selected, **then** green checkmark appears | P0 | US‑U1 |
| **US‑U3** | *As a user, I want the upload table to list Filename, Detected Type, Target Sheet, Status.* | ▸ **Given** queued files, **when** table renders, **then** four columns render for each file. ▸ **Given** narrow mobile width ≤ 375 px, **when** I rotate phone, **then** the table stacks responsively without horizontal scroll. **Given** file uploaded, **when** processing starts, **then** status shows "Processing" Given processing complete, when successful, then status shows "Done" with row count Given processing fails, when error occurs, then status shows "Error" with tooltip Given tablet width ≈ 768 px, when viewing, then columns fit without horizontal scroll.  Given desktop ≥ 1280 px, when viewing, then full table displays with balanced column widths. | P0 | US‑U1 |
| **US‑U4** | *As a user, I can override the auto‑selected target sheet via dropdown so that I keep control.* | ▸ **Given** a queued file, **when** I click the Target dropdown, **then** all sheet names from my workbook appear. ▸ **Given** I choose a sheet, **when** selection closes, **then** the Target column shows my choice. ▸ **Given** override selected, **when** processing runs, **then** rows are written to that sheet. | P1 | US‑U3 |
| **US‑U5** | *As a user, I see real‑time upload progress so that I know what’s happening.* | ▸ **Given** a file upload in flight, **when** bytes stream, **then** a progress bar shows percentage until 100 %. ▸ **Given** backend processing begins, **when** extraction runs, **then** the Status badge switches to **Processing** with spinning icon. ▸ **Given** processing finishes, **when** success, **then** badge shows **Done (n rows)** else **Error** with tooltip. | P0 | US‑U3 |
| **US‑U6** | *As a user, I receive toast notifications summarising completion or failure.* | ▸ **Given** all queued files finish, **when** any file failed, **then** a red toast lists each failed filename. ▸ **Given** all succeed, **when** final callback fires, **then** a green toast shows total rows inserted. ▸ **Given** I click a toast, **when** clicked, **then** it links to detailed run log modal. | P1 | US‑U5 |
| **US‑U7** | *As a user, I want to tag Budget transactions via dropdown (Fola, Pippa, Ileri, Tami) so that the Tag column is pre‑populated.* | Given Budget preview open, when I select one or more rows, then a Tag dropdown appears with four names.   Given I choose Fola and click Apply, then Tag column of selected rows updates to Fola.   Given I confirm the upload, when rows write, then Tag values persist in the sheet. | P1 | US‑P1 |

---

## **Epic 3 – Data Preview & Confirmation**

| ID | User Story | Acceptance Criteria | Priority | Dependencies |
| ----- | ----- | ----- | ----- | ----- |
| **US‑P1** | *As a user, I want to preview extracted rows before they hit Sheets so that I can verify accuracy.* | ▸ **Given** extraction succeeds, **when** I click **Preview**, **then** a modal opens showing the first 100 rows with sticky headers. ▸ **Given** I scroll the modal, **when** reaching bottom, **then** virtual scrolling loads more rows without lag. ▸ **Given** extraction fails, **when** I click Preview, **then** an error banner **“Cannot preview – extraction error”** is shown. | P1 | US‑E4 |
| **US‑P2** | *As a user, I can confirm or abort the upload from the preview so that I stay in control.* | ▸ **Given** preview modal open, **when** I click **Confirm**, **then** rows proceed to transformation pipeline. ▸ **Given** I click **Abort**, **when** confirmed, **then** the file status changes to **Cancelled** and no rows are written. ▸ **Given** operation completes, **when** modal closes, **then** a toast summarises the action. | P1 | US‑P1 |

---

## **Epic 4 – Extraction Pipeline**

| ID | User Story | Acceptance Criteria | Priority | Dependencies |
| ----- | ----- | ----- | ----- | ----- |
| **US‑E1** | *As the system, I want to parse Monzo CSVs into Budget‑schema rows so that they can be written to the sheet.* | ▸ **Given** a sample Monzo export, **when** parsed, **then** 100 % rows map to 17 expected columns. ▸ **Given** a malformed CSV, **when** parser hits error, **then** a structured error is returned with line number. ▸ **Given** valid CSV, **when** unit tests run, **then** they pass with ≥ 95 % code coverage. | P0 | US‑U5 |
| **US‑E2** | *As the system, I want to extract relevant financial data from **PDF statements** using a multimodal LLM first, pdfplumber second.* | Given a PDF statement, when processed by GPT‑4o / Claude / Gemini, then ≥ 95 % of required data fields (date, description, amount, etc.) correctly extracted.  Given LLM extraction fails (\< 90 % integrity or error), when fallback triggers, then pdfplumber extracts the required fields. Given both methods fail, when error thrown, then user sees Error badge with tooltip. | P0 | US‑U5 |
| **US‑E3** | *As the system, I want to extract relevant financial data from images (PNG/JPG) using a multimodal LLM, Tesseract fallback.* | Given a screenshot image, when sent to multimodal LLM vision endpoint, then ≥ 90 % of required data fields captured accurately.   Given LLM extraction confidence \< 70 % or error, when fallback triggers, then Tesseract OCR runs.   Given both methods fail, when error thrown, then user receives Image extraction error toast. | P0 | US‑U5 |
| **US‑E4** | *As the system, I want to auto‑detect file type to route to the correct extractor.* | Given a CSV, when MIME sniffing runs, then fileType = CSV and extractor = E1 invoked.   Given a PDF, when sniffer runs, then extractor = E2 invoked.   Given an image (PNG/JPG), when sniffer runs, then extractor = E3 invoked. | P0 | US‑E1 E2 E3 |

---

## **Epic 5 – Transformation & Deduplication**

| ID | User Story | Acceptance Criteria | Priority | Dependencies |
| ----- | ----- | ----- | ----- | ----- |
| **US‑T1** | *As the system, I want to map Portfolio rows to the common schema so that data aligns with Sheets.* | ▸ **Given** raw rows, **when** mapping runs, **then** all mandatory columns (**Asset, Units, Price…**) are populated. ▸ **Given** optional field missing, **when** mapping, **then** defaults (empty string / 0\) are applied. ▸ **Given** mapping complete, **when** schema validator runs, **then** no errors are returned. Given formula columns, when mapping, then left blank for sheet formulas | P0 | US‑E2 E3 |
| **US‑T2** | *As the system, I want to copy Budget CSV rows verbatim plus a Tag column so that formulas can populate tags later.* | ▸ **Given** transform runs, **when** unit tests execute, **then** 100 % rows preserved. Given Budget CSV rows, when transform runs, then original 17 columns plus Tag are output.   Given Tag values selected in UI, when transform executes, then those values persist in Tag column.   Given row without Tag, when transform runs, then Tag value \= empty string. | P0 | US‑E1 |
| **US‑T3** | *As the system, I want to deduplicate rows via hash so that duplicates are not re‑inserted.* | ▸ **Given** rows with identical hash, **when** check runs, **then** only the first instance is marked **Insert**, others **Duplicate**. ▸ **Given** duplicate detected, **when** UI polls, **then** Status badge \= **Duplicate** and tooltip shows existing row id. ▸ **Given** new upload with same content, **when** dedup runs, **then** zero rows are appended. | P0 | US‑T1 T2 |

---

## **Epic 6 – Google Sheets Writer**

| ID | User Story | Acceptance Criteria | Priority | Dependencies |
| ----- | ----- | ----- | ----- | ----- |
| **US‑S0** | *As the system, I want to connect to the Google Sheets API so that subsequent write operations work.* | Given a valid OAuth token, when client initialises, then Sheets service returns OK.   Given connection established, when I request sheet metadata, then response arrives within 2 s. Given transient network error, when retry logic triggers, then exponential back‑off (2,4,8 s) applied up to 3 times. | P0 | US‑A1 |
| **US‑S1** | *As the system, I want to append rows below the header so that existing data is preserved.* | ▸ **Given** valid OAuth token, **when** append API call executes, **then** new rows start at first blank line. ▸ **Given** header row frozen, **when** append runs, **then** row 1 remains untouched & frozen. Given write complete, when verifying, then row count increases correctly | P0 | US‑S0 T1 T2 |
| **US‑S2** | *As the system, I want to lock the header row after insert so that users don’t accidentally edit it.* | ▸ **Given** new sheet, **when** first append runs, **then** header row is set to **protectedRange** via API. ▸ **Given** protection exists, **when** subsequent appends run, **then** they respect the protection. ▸ **Given** header editing attempt, **when** user tries in UI, **then** Google shows *“You can’t edit protected cell”*. | P0 | US‑S1 |
| **US‑S3** | *As the system, I want to batch‑append large sets with exponential back‑off so that rate limits are respected.* | Given \>100 rows, when writing, then data batched in 500-row chunks ▸ **Given** quota error, **when** retry logic triggers, **then** back‑off (2,4,8 s) is applied and call eventually succeeds. ▸ **Given** permanent failure after 3 retries, **when** aborts, **then** detailed error returned to UI. | P1 | US‑S1 |

---

## **Epic 7 – Formula Propagation**

| ID | User Story | Acceptance Criteria | Priority | Dependencies |
| ----- | ----- | ----- | ----- | ----- |
| **US‑F0** | *As the system, I want to detect formula columns so that I know what needs propagation.* | Given the Budget Tagging sheet, when analyser runs, then formula columns are identified and returned as an array.   Given formulas found, when patterns are extracted, then they match existing formulas exactly. Given no formulas found, when checking, then the propagation step is skipped. | P0  | US‑S1 |
| **US‑F1** | *As the system, I want to fill‑down formulas in Budget Tagging so that calculated fields stay in sync.* | ▸ **Given** new rows, **when** append completes, **then** formulas in Tagging sheet expand to same row count. ▸ **Given** formulas extend, **when** relative refs adjust, **then** test sheet shows correct calculated values. ▸ **Given** propagation fails, **when** error thrown, **then** event logged and retry performed once. | P0 | US‑F0 |
| **US‑F2** | *As the system, I want to validate formula propagation and re‑run on mismatch so that integrity is guaranteed.* | ▸ **Given** fill‑down done, **when** validator counts non‑empty formula cells, **then** count equals Budget sheet rows. ▸ **Given** mismatch detected, **when** validator triggers, **then** fill‑down reruns automatically. ▸ **Given** second failure, **when** occurs, **then** user receives **Formula error** toast. | P0 | US‑F1 |

---

## **Epic 8 – LLM Category Suggestion**

| ID | User Story | Acceptance Criteria | Priority | Dependencies |
| ----- | ----- | ----- | ----- | ----- |
| **US‑L1** | *As the system, I want to find Budget rows where Retag is blank so that I can suggest categories.* | ▸ **Given** Tagging sheet, **when** scan runs, **then** blank Retag cells are collected in a batch payload. ▸ **Given** no blanks found, **when** scan completes, **then** pipeline ends with **No action** status. ▸ **Given** blanks found, **when** payload prepared, **then** rows proceed to LLM prompt. | P1 | US‑F1 |
| **US‑L2** | **As a** system **I want** to generate category suggestions **So that** users have intelligent help | • Given transaction notes/tags, when prompting LLM, then category suggested • Given category list, when suggesting, then only valid categories used\<br\> • Given LLM response, when parsing, then suggestion formatted correctly | P1 | US‑L1 |
| **US‑L3** | *As the system, I want to write suggestions to “Retag Suggested (LLM)” so that users can review.* | ▸ **Given** suggestion set, **when** Sheets batch update runs, **then** column populated next to each blank cell. ▸ **Given** suggestions, **when** write completes, **then** row count matches. ▸ **Given** write error, **when** occurs, **then** failed writes retried once and error surfaced if persistent. | P1 | US‑L2 |

---

## **Epic 9 – Observability & Error Handling**

| ID | User Story | Acceptance Criteria | Priority | Dependencies |
| ----- | ----- | ----- | ----- | ----- |
| **US‑O1** | *As an engineer, I want structured JSON logs for every pipeline step so that issues are traceable.* | ▸ **Given** a successful run, **when** logs viewed, **then** each stage emits `stage, fileId, durationMs, status` fields. ▸ **Given** a failure, **when** it occurs, **then** log level \= ERROR and stack trace included. ▸ **Given** log filters, **when** I query `fileId`, **then** all related entries appear chronologically. | P1 | — |
| **US‑O2** | *As an engineer, I want Sentry error tracking integrated so that uncaught exceptions alert the team.* | ▸ **Given** an exception, **when** raised, **then** Sentry issue created with environment tag (prod/stage). ▸ **Given** issue resolved in code, **when** redeployed, **then** Sentry auto‑resolves. ▸ **Given** duplicate exception, **when** occurs, **then** Sentry groups it under existing issue. | P1 | — |
| **US‑O3** | *As a user, I want status badges to reflect backend errors so that I understand what went wrong.* | ▸ **Given** backend returns 500, **when** UI polls status, **then** badge \= **Error** with hover tooltip from error message and tooltip shows user‑friendly message. ▸ **Given** backend retried & succeeds, **when** status updates, **then** badge turns **Done** automatically. ▸ **Given** error persists, **when** I click badge, **then** log modal opens filtered by fileId. Given error supports retry, when badge clicked, then modal explains steps and offers Retry. | P1 | US‑O1 O2 |

---

## **Epic 10 – UX Polish & Performance**

| ID | User Story | Acceptance Criteria | Priority | Dependencies |
| ----- | ----- | ----- | ----- | ----- |
| **US‑X1** | *As a user, I want a brand‑neutral light theme so that the UI feels professional on any device.* | ▸ **Given** dashboard load, **when** inspected, **then** Tailwind utility classes implement neutral palette (\#f9fafb–\#1f2937). ▸ **Given** prefers‑color‑scheme dark, **when** not supported, **then** UI still meets WCAG AA contrast. ▸ **Given** 375 px mobile width, **when** viewed, **then** no horizontal scroll bars appear. | P2 | US‑U3 |
| **US‑X2** | *As a user, I want end‑to‑end processing of ≤ 200 rows to finish in under 10 s so that the app feels snappy.* | ▸ **Given** 200‑row CSV, **when** stopwatch starts at upload, **then** **Done** badge shows ≤ 10 s later in staging env. ▸ **Given** performance test, **when** P95 latency \> 10 s, **then** task fails CI perf gate. ▸ **Given** perf optimisation, **when** code changes, **then** regression test reruns automatically. | P2 | All pipeline stories |
| **US‑X3** | *As a user, I want clear loading states and feedback so that I know the app is working.* | Given an operation expected \> 0.5 s, when it starts, then a loading spinner appears within 100 ms.  Given operation completes, when success, then spinner fades out and success toast appears within 200 ms.  Given operation fails, when error thrown, then spinner replaced by red error banner with details. | P1 | US‑U5 |
| **US‑X4** | *As a user, I want responsive layout across mobile, tablet and desktop so the whole app is usable everywhere.* | Given 375 px viewport, when navigating any page, then no content overflows horizontally. Given 768 px viewport, when navigating, then two‑column layout engaged. Given ≥ 1280 px viewport, when navigating, then layout stretches to max 1440 px and centres content. | P1 | US‑U3 |

---

