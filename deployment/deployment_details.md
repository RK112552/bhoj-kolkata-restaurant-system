# Deployment Details

## Before deployment
- [ ] Replace all demo passwords.
- [ ] Set a strong random `FLASK_SECRET_KEY` in the hosting provider's secret settings.
- [ ] Create a production MySQL database and least-privilege DB user.
- [ ] Set environment variables; do not commit `.env`.
- [ ] Set `FLASK_DEBUG=false`.
- [ ] Enable HTTPS.
- [ ] Configure database backups and log monitoring.
- [ ] Add CSRF protection, rate limiting, secure cookies and production WSGI server.
- [ ] Test all roles using non-sensitive sample data.

## Suggested deployment approach
1. Push the repository to GitHub.
2. Provision a Python-compatible web host and a MySQL-compatible database host.
3. Configure environment variables from `.env.example`.
4. Run the SQL scripts in order against the hosted database.
5. Set the start command to a production WSGI server such as `gunicorn src.backend.app:app` after making the project import path compatible with the host (or deploy from the `src/backend` directory with `gunicorn app:app` and `PYTHONPATH` configured).
6. Verify `/health`, login, menu reads, a reservation, an order, and database-backed reporting.
7. Record the live URL, GitHub URL, commit hash/date, and screenshots here.

Live website URL: _Add after deployment_  
GitHub repository URL: _Add after creating repository_  
Deployment date / commit: _Add after deployment_
