---
description: How to deploy this application to Render.com
---
This project is configured for deployment on Render, a cloud hosting platform. Be sure you have a Render account and a GitHub/GitLab repository connected to it.

## Prerequisites
1.  **Git Repository**: Ensure your code is pushed to a remote repository (GitHub, GitLab, or Bitbucket).
2.  **Render Account**: Sign up at [dashboard.render.com](https://dashboard.render.com).

## Deployment Steps

### 1. Create a New Web Service
1.  On the Render Dashboard, click **New +** -> **Web Service**.
2.  Select "Build and deploy from a Git repository".
3.  Connect your repository (e.g., `Joelseph2405/missouri-territory-map`).

### 2. Configure the Service
Render should automatically detect the configuration from `render.yaml`. If it doesn't, ensure the following settings:
-   **Name**: `territory-map` (or your preferred name)
-   **Runtime**: `Python 3`
-   **Build Command**: `pip install -r requirements.txt`
-   **Start Command**: `gunicorn app:app`

### 3. Database Setup (Crucial)
This application requires a database. You have two options:

#### Option A: PostgreSQL (Recommended for Production)
1.  On Render Dashboard, click **New +** -> **PostgreSQL**.
2.  Give it a name (e.g., `territory-db`).
3.  Create the database.
4.  Copy the **Internal Database URL** from the database settings.
5.  Go to your Web Service (**territory-map**) -> **Environment**.
6.  Add an environment variable:
    -   Key: `DATABASE_URL`
    -   Value: `[Paste your Internal Database URL]`
7.  Deploy/Redeploy the Web Service. The app will detect the `DATABASE_URL` and switch to Postgres mode automatically.

#### Option B: SQLite (Simpler, but with data persistence caveats)
By default, Render Web Services have ephemeral filesystems. If you use SQLite (default if no `DATABASE_URL` is set), your data (notes, new businesses) will be reset every time you deploy.
To persist SQLite data:
1.  Go to your Web Service -> **Disks**.
2.  Add a Disk.
    -   **Mount Path**: `/var/lib/data`
    -   **Size**: 1GB (sufficient for this app).
3.  The application is already configured to look for the database at `/var/lib/data/businesses.db` if valid.

## Automatic Database Initialization
On the first run, the application will automatically:
1.  Create the necessary database tables.
2.  Import the initial data from `data/businesses.json`.

## Verification
1.  Wait for the deployment to finish (Green "Live" badge).
2.  Click the URL provided by Render (e.g., `https://territory-map.onrender.com`).
3.  The map should load with your businesses.
