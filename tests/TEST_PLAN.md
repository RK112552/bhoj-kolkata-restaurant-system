# Test Plan

Run tests against a disposable local database before deployment.

| ID | Test | Expected result |
|---|---|---|
| T01 | Open home/menu without login | Public menu appears |
| T02 | Login with valid customer account | Customer account page opens |
| T03 | Login with invalid password | Friendly error; no session |
| T04 | Customer opens `/dashboard` | HTTP 403; no revenue data |
| T05 | Kitchen opens menu management | HTTP 403 |
| T06 | Manager adds a menu item | Item appears in database and public menu |
| T07 | Manager hides a menu item | Item no longer appears publicly |
| T08 | Submit reservation with required fields | Pending reservation inserted |
| T09 | Submit reservation without phone/time | Validation message |
| T10 | Customer submits order with quantities | Order, order items and bill created together |
| T11 | Simulate a database error during order placement | Transaction rolls back |
| T12 | Kitchen changes order to preparing/ready | Updated status visible in order list |
| T13 | Cashier records demo payment | Payment inserted and bill marked paid |
| T14 | Attempt to mark an already paid bill paid again | Duplicate payment prevented by application check |
| T15 | Query `vw_daily_sales` | Aggregated completed payments returned |
| T16 | Run correlated menu price query | Only items above their category average returned |
| T17 | Call `sp_update_order_status` with invalid status | SQL error is raised |
| T18 | Insert/update ORDER_ITEMS | Trigger recalculates order total |
| T19 | Search and filter menu | Results match search/category |
| T20 | Resize browser to mobile width | Navigation and content remain usable |

Record actual results, date, tester and screenshot for the final report.
