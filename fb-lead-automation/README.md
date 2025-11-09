# Facebook Lead Generation Automation App

A complete automation application that automatically sends personalized messages to users who interact with Facebook/Instagram ads through Lead Forms.

## Features

- **Automated Lead Capture**: Automatically receive leads from Facebook Lead Forms via webhooks
- **Personalized Messaging**: Send customized messages to leads using templates with placeholders
- **Ad Synchronization**: Background job syncs active ads from Facebook every 10 minutes
- **Template Management**: Create and manage message templates for each ad
- **Lead Tracking**: Track all leads and message delivery status
- **Statistics Dashboard**: View lead conversion metrics and success rates
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS

## Tech Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database
- **APScheduler**: Background job scheduling
- **Flask-CORS**: Cross-origin resource sharing
- **Flask-Migrate**: Database migrations
- **Requests**: HTTP library for API calls

### Frontend
- **React**: UI library
- **Vite**: Build tool and dev server
- **React Router**: Client-side routing
- **React Query**: Data fetching and caching
- **Axios**: HTTP client
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Icon library
- **date-fns**: Date formatting

## Project Structure

```
fb-lead-automation/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # App factory
│   │   ├── config.py            # Configuration
│   │   ├── extensions.py        # Flask extensions
│   │   ├── models/              # Database models
│   │   │   ├── ad.py
│   │   │   ├── message_template.py
│   │   │   └── lead.py
│   │   ├── routes/              # API endpoints
│   │   │   ├── ads.py
│   │   │   ├── messages.py
│   │   │   ├── leads.py
│   │   │   └── webhook.py
│   │   ├── services/            # Business logic
│   │   │   ├── facebook_service.py
│   │   │   ├── messenger_service.py
│   │   │   └── template_service.py
│   │   └── jobs/                # Background jobs
│   │       └── ad_sync_job.py
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── ads/
│   │   │   ├── messages/
│   │   │   └── leads/
│   │   ├── pages/               # Page components
│   │   ├── services/            # API services
│   │   ├── hooks/               # Custom React hooks
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── README.md
```

## Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- Facebook App with Marketing API access
- Facebook Page with Messenger access

### Backend Setup

1. Navigate to the backend directory:
```bash
cd fb-lead-automation/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from the example:
```bash
cp .env.example .env
```

5. Edit `.env` and add your Facebook credentials:
```env
SECRET_KEY=your-secret-key
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
FACEBOOK_ACCESS_TOKEN=your_access_token
FACEBOOK_AD_ACCOUNT_ID=your_ad_account_id
PAGE_ACCESS_TOKEN=your_page_access_token
VERIFY_TOKEN=your_custom_verify_token
```

6. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

7. Run the backend server:
```bash
python run.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd fb-lead-automation/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file (optional):
```bash
cp .env.example .env
```

4. Run the development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

## Configuration

### Environment Variables

#### Backend (.env)

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key for session management | Yes |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |
| `FACEBOOK_APP_ID` | Facebook App ID | Yes |
| `FACEBOOK_APP_SECRET` | Facebook App Secret | Yes |
| `FACEBOOK_ACCESS_TOKEN` | Facebook Marketing API access token | Yes |
| `FACEBOOK_AD_ACCOUNT_ID` | Facebook Ad Account ID (without 'act_' prefix) | Yes |
| `PAGE_ACCESS_TOKEN` | Facebook Page access token for Messenger | Yes |
| `VERIFY_TOKEN` | Custom token for webhook verification | Yes |
| `AD_SYNC_INTERVAL_MINUTES` | Interval for syncing ads (default: 10) | No |
| `CORS_ORIGINS` | Allowed CORS origins (default: http://localhost:3000) | No |

#### Frontend (.env)

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_URL` | Backend API URL | No (defaults to http://localhost:5000) |

### Facebook App Setup

1. **Create a Facebook App**:
   - Go to [Facebook Developers](https://developers.facebook.com/)
   - Create a new app with Marketing API access

2. **Configure Webhooks**:
   - Add webhook subscription for `leadgen` events
   - Set webhook URL to `https://your-domain.com/api/webhook`
   - Use the same `VERIFY_TOKEN` from your `.env` file

3. **Get Access Tokens**:
   - **Marketing API Token**: Use Facebook Graph API Explorer
   - **Page Access Token**: Get from your Facebook Page settings

4. **Subscribe to Lead Forms**:
   - Subscribe your app to lead forms on your Facebook Page

## API Endpoints

### Ads

- `GET /api/ads` - Get all ads
- `GET /api/ads/:id` - Get specific ad
- `POST /api/ads/sync` - Manually sync ads from Facebook
- `DELETE /api/ads/:id` - Delete ad

### Messages

- `GET /api/messages` - Get all message templates
- `GET /api/messages/:id` - Get specific template
- `POST /api/messages` - Create template
- `PUT /api/messages/:id` - Update template
- `DELETE /api/messages/:id` - Delete template
- `POST /api/messages/:id/preview` - Preview template with sample data

### Leads

- `GET /api/leads` - Get all leads (paginated)
- `GET /api/leads/:id` - Get specific lead
- `GET /api/leads/stats` - Get lead statistics

### Webhook

- `GET /api/webhook` - Webhook verification endpoint
- `POST /api/webhook` - Receive lead events from Facebook

## Usage

### 1. Sync Ads

1. Navigate to the **Ads** page
2. Click the **Sync Ads** button
3. The app will fetch all active ads from your Facebook account

### 2. Create Message Templates

1. Click on an ad card
2. Create a new template or edit existing one
3. Use placeholders like `{{first_name}}`, `{{last_name}}`, `{{email}}`, `{{phone}}`
4. Add custom variables for additional personalization
5. Preview the message
6. Save the template

### 3. Receive Leads

When a user submits a lead form:
1. Facebook sends a webhook event
2. The app fetches lead data
3. Finds the message template for that ad
4. Fills template with lead data
5. Sends personalized message via Messenger
6. Saves lead to database

### 4. Track Leads

1. Navigate to the **Leads** page
2. View statistics and lead list
3. Check message delivery status

## Message Template Placeholders

### Standard Placeholders

- `{{first_name}}` - Lead's first name
- `{{last_name}}` - Lead's last name
- `{{email}}` - Lead's email address
- `{{phone}}` - Lead's phone number

### Custom Variables

You can add custom variables for each template:
- `{{product_name}}` - Product being advertised
- `{{discount}}` - Special offer discount
- `{{company_name}}` - Your company name
- Any other custom placeholder

## Background Jobs

### Ad Sync Job

Runs every 10 minutes (configurable) to:
- Fetch active ads from Facebook
- Update existing ads
- Create new ads
- Mark missing ads as inactive (doesn't delete)

## Database Schema

### Ad Table
- `id`: Primary key
- `ad_id`: Facebook ad ID (unique)
- `ad_name`: Ad name
- `campaign_id`, `campaign_name`: Campaign info
- `adset_id`, `adset_name`: Ad set info
- `status`: Ad status (ACTIVE, PAUSED, etc.)
- `is_active`: Local active status
- `last_synced_at`: Last sync timestamp

### MessageTemplate Table
- `id`: Primary key
- `ad_id`: Foreign key to Ad (unique)
- `template_name`: Template name
- `message_text`: Template with placeholders
- `variables`: Custom variables (JSON)
- `is_active`: Active status

### Lead Table
- `id`: Primary key
- `lead_id`: Facebook lead ID (unique)
- `ad_id`: Foreign key to Ad
- `user_fb_id`: Facebook user ID
- `user_name`: User's name
- `message_sent`: Delivery status
- `message_text`: Sent message
- `metadata`: Lead form data (JSON)

## Troubleshooting

### Backend Issues

**Database errors:**
```bash
# Reset database
rm app.db
flask db upgrade
```

**Import errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Facebook API errors:**
- Check if access tokens are valid
- Verify ad account ID is correct (without 'act_' prefix)
- Ensure app has necessary permissions

### Frontend Issues

**Build errors:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API connection errors:**
- Verify backend is running on port 5000
- Check CORS settings in backend config
- Ensure API URL is correct in frontend

### Webhook Issues

**Webhook not receiving events:**
- Verify webhook URL is accessible from internet
- Check if VERIFY_TOKEN matches
- Ensure app is subscribed to leadgen events
- Test with ngrok for local development

## Development

### Running Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Building for Production

#### Backend
```bash
# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

#### Frontend
```bash
npm run build
# Deploy dist/ folder to your hosting
```

## Security Considerations

- Never commit `.env` files
- Use strong `SECRET_KEY` in production
- Validate webhook signatures
- Use HTTPS in production
- Rotate access tokens regularly
- Limit CORS origins in production

## License

MIT License

## Support

For issues and questions:
- Check the troubleshooting section
- Review Facebook API documentation
- Open an issue on GitHub

## Success Criteria

- ✅ Backend starts without errors
- ✅ Frontend compiles and runs
- ✅ All API endpoints are accessible
- ✅ Database migrations work
- ✅ UI displays correctly with Tailwind
- ✅ Navigation works between pages
- ✅ Forms can be submitted
- ✅ Data is saved to SQLite database
- ✅ Background scheduler initializes

## Next Steps

1. Connect to Facebook APIs with your credentials
2. Set up webhook in Facebook App
3. Test with sample lead form
4. Monitor leads and messages
5. Deploy to production server

---

Built with ❤️ using Flask and React
