# Careplans operation catalog

Use this reference to choose a supported operation and its parameters. The current connection's advertised tools, schemas, permissions and preview are authoritative; this catalog does not make an unavailable capability callable.

## Reads used to select rows

All six searches take the exact `careplan_id` and optionally `name` to filter row names.

| Tool | Relevant scope |
| --- | --- |
| `careplans_search_rows` | Active, non-completed rows; excludes completed, removed and deleted rows |
| `careplans_completed_rows` | Completed prestations, including candidates for a requested refund/storno |
| `careplans_pending_rows` | Candidates for pending cleanup |
| `careplans_ethics_rows` | Candidates for ethics/non-execution changes |
| `careplans_restorable_rows` | Removed or disabled rows eligible for restoration |
| `careplans_code_rows` | Rows relevant to code disabling |

Queries describe different subsets. Use additional relevant queries when the requested scope spans them. No match in one subset is not proof of absence from every subset. Respect result limits and report when the complete requested set could not be retrieved. Combining read results does not combine their write eligibility: the current price-update, laboratory-cost and row-deletion operations accept only rows eligible through `careplans_search_rows`, not completed rows.

## Ten preview operations

Every preview requires `careplan_id` and `numero_ticket`. The extra fields below are the only operation-specific fields; execution later takes only the returned `previewId` and `confirm: true`.

| Intended change | Preview tool | Extra fields | Target and effect to verify |
| --- | --- | --- | --- |
| Storno/refund | `careplans_preview_refund` | `row_ids` | Read completed rows and check the selected prestations. Review the preview's negative and replacement-row effects. |
| Pending cleanup | `careplans_preview_clear_pending` | `row_ids` | Use the pending query; “all uncompleted rows” is not an equivalent eligibility rule. |
| Ethics/non-execution change | `careplans_preview_clear_ethics` | `row_ids` | Use the ethics query and check the exact intended effect in the preview. |
| Unlock plan | `careplans_preview_unlock` | None | Plan-wide operation. Verify the target plan and preview; do not supply row IDs. |
| Set net prices | `careplans_preview_update_prices` | `row_ids`, `prezzo` | Absolute new net price per selected eligible non-completed row from the search query. Completed rows are outside this operation's current scope. |
| Delete rows | `careplans_preview_delete_rows` | `row_ids` | Select eligible non-completed rows from the search query and verify the deletion effect. Do not substitute plan-wide complaint deletion. |
| Set laboratory costs | `careplans_preview_update_lab_costs` | `row_ids`, `lab_price` | Absolute new laboratory cost per selected eligible non-completed row from the search query, distinct from net price. |
| Delete complaint/lamentela | `careplans_preview_delete_complaint` | None | Plan-wide operation. Review related rows and records shown in the preview; a row deletion is a different request. |
| Restore rows | `careplans_preview_restore_rows` | `row_ids` | Use the restorable query; active-row context does not establish this set. |
| Disable codes | `careplans_preview_disable_codes` | `row_ids` | Use the code query. Affected codes can outnumber selected rows; verify the receipt's actual count. |

Use positive safe-integer IDs as returned by the connection. Row lists contain 1–200 unique IDs under this contract; never silently drop excess rows or duplicates to make a request fit. Follow the live schema if it advertises a different bound, and agree a scoped approach when one operation cannot cover the intended set.

For price, laboratory-cost or deletion requests that include completed rows, read the completed subset to identify the unsupported scope. Do not send those IDs to the corresponding preview or silently act on only the eligible subset. Clarify whether a supported non-completed-only change is intended; otherwise report that the requested change cannot be completed with this operation.

The ticket reference is nonempty text with no control characters, up to 120 characters. Prices and laboratory costs are finite nonnegative amounts, up to the live schema's maximum. Omit fields not accepted by the selected preview; do not send a percentage, arbitrary payload, SQL, endpoint, actor ID or operation ID.

## Confirmation and recovery tools

- `careplans_execute_operation`: `{ previewId, confirm: true }`. Use the returned preview unchanged and before its advertised expiry, with explicit permission for its operation.
- `careplans_operation_status`: `{ previewId }`. Retrieve or reconcile the original operation outcome. An unresolved outcome does not authorize a fresh operation or prove that no change occurred.

Keep these runtime identifiers private to the authorized task. Neither tool requires raw credentials as an argument.
