# Full-Stack Flask eCommerce Store with Stripe Integration

A secure, production-ready full-stack eCommerce application built in Python using Flask that demonstrates session-based state management, mutable array tracking, and secure server-to-server transaction delegation using Stripe Checkout.

## 🚀 Architecture & Transaction Flow
* **Stateful Cart Session Architecture:** Manages user shopping carts securely on the server-side via cookie-encrypted session memory layers. It uses explicit mutation flags (`session.modified = True`) to reliably track item additions in real-time.
* **Tokenized Gateway Redirection:** Translates client checkout selections into tokenized line-item arrays, delegating card data handling to external Stripe Hosted Checkout fields. This entirely eliminates local payment storage liabilities.
* **Idempotent Status Handlers:** Features isolated, verification-safe success and failure routing paths to guarantee that local cart arrays flush correctly upon verified captures or preserve state on intentional cancellations.

## 🛠️ Software Stack
* **Language Environment:** Python 3.x
* **Core Subsystems:** Flask Microframework, Official Stripe SDK, Jinja2 Template Compilers
