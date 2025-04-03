# Deploying BrokeNoMore to Render

## Option 1: Deploy using the Render Dashboard

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" and select "Web Service"
3. Connect your GitHub repository or use the public URL
4. Configure your service with the following settings:
   - Name: broke-no-more-backend (or your preferred name)
   - Runtime: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add the following environment variables:
   - All environment variables from your `.env` file

## Option 2: Deploy using render.yaml (Blueprint)

1. Ensure your repository contains the `render.yaml` file
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New" and select "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect the `render.yaml` file and deploy the service
6. Add the necessary environment variables from your `.env` file

## Option 3: Deploy using Docker

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" and select "Web Service"
3. Select "Deploy from Docker image"
4. Connect your GitHub repository (with Dockerfile)
5. Add the necessary environment variables from your `.env` file

## Important Notes

- Ensure all environment variables in your `.env` file are added to Render's environment variables
- For database connections, if using Supabase, make sure to update the connection strings
- Set `PORT` to the value Render assigns (usually done automatically)
- For production, set appropriate environment variables like `DEBUG=False` 