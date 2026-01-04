# New Features Implementation Guide

This document outlines the new advanced features added to your Missouri Territory Map application.

## Features Overview

### 1. Contact Management System
- Multiple contacts per business
- Track names, titles, phone, email
- Primary contact designation
- Contact notes and decision-maker flags

### 2. Business Card Scanner (OCR)
- Camera/upload photo of business card
- Tesseract.js OCR extracts contact information
- Auto-creates contact and adds to business
- No photo storage - data only

### 3. Enhanced Visit Tracking
- **Who you met with** (dropdown from contacts)
- **Activity type** (Sales Call, Discovery, Demo, etc.)
- **Opportunity notes** (separate field for deals/follow-ups)
- All tracked for daily reports

### 4. Smart Business Lookup with External Database & Geolocation
- **Works with BOTH voice AND typing:**
  - Say business name during voice-guided entry
  - **OR** Type business name in the form and click "🔍 Search" button
- **Searches TWO sources automatically:**
  - Your local database (existing businesses you've added)
  - **OpenStreetMap public database** (millions of businesses in Missouri)
- **📍 Flexible location options:**
  - **Option 1: Enter your zip code** (recommended for desktop users)
    - Type your current zip code in the "Your Location Zip Code" field
    - More accurate than GPS on desktop computers
    - Example: Enter "63301" if you're in St. Charles
  - **Option 2: Use GPS** (recommended for mobile users)
    - Leave zip code field blank
    - Browser will request your GPS location
    - Better accuracy on mobile devices
  - Prioritizes businesses closest to you
  - Shows distance in miles for each suggestion
  - Results sorted by proximity (nearest first)
- **Manual search trigger:**
  - Type business name (at least 3 characters)
  - Click "🔍 Search" button when ready
  - No auto-suggestions while typing (you control when to search)
- Shows up to 5 suggestions with badges:
  - 💾 Your Database (green) = Businesses you've already added
  - 📡 Public Database (yellow) = Businesses from OpenStreetMap
  - 📍 Distance badge (blue) = Shows how far away (e.g., "2.3 mi away")
- **Auto-fills ALL details** when you select a match:
  - Business name, address, city, zip code
  - Phone number (if available in public data)
  - GPS coordinates for map placement
- Much faster than manual entry - minimal typing required!
- **Completely free** - no API keys or costs
- **Privacy-first**: Location only used for search, not stored

### 5. Daily Activity Email Reports
- **Automatically sends at 5:30 PM CST daily**
- Sent from your Gmail account via EmailJS
- Includes:
  - All businesses visited today
  - Who you met with at each
  - Activity type
  - Opportunities identified
  - Follow-up actions needed

## Setup Required

### Gmail/EmailJS Setup (One-Time)

To enable daily email reports from your Gmail account:

1. **Create EmailJS Account** (Free):
   - Go to https://www.emailjs.com/
   - Sign up with your Gmail account
   - Free tier allows 200 emails/month (plenty for daily reports)

2. **Get Your EmailJS Credentials**:
   You'll need 3 things:
   - Service ID
   - Template ID
   - Public Key (User ID)

3. **Detailed Setup Steps**:

   a. **After signing up**, go to Email Services
      - Click "Add New Service"
      - Choose "Gmail"
      - Connect your Gmail account
      - Copy your **Service ID** (something like 'service_xxxxxxx')

   b. **Create Email Template**:
      - Go to Email Templates
      - Click "Create New Template"
      - Name it "Daily Territory Report"
      - Use this template:

      ```
      Subject: Territory Report - {{report_date}}

      From: {{from_name}}

      {{message_html}}
      ```

      - Copy your **Template ID** (something like 'template_xxxxxxx')

   c. **Get Public Key**:
      - Go to Account → General
      - Copy your **Public Key** (under API Keys)

4. **Add Credentials to index.html**:
   - Open index.html
   - Find the section marked `// EmailJS Configuration`
   - Replace the placeholders with your actual values:

   ```javascript
   const EMAIL_CONFIG = {
       serviceId: 'service_xxxxxxx',     // Your Service ID
       templateId: 'template_xxxxxxx',   // Your Template ID
       publicKey: 'your_public_key',     // Your Public Key
       userEmail: 'your.email@gmail.com' // Your Gmail address
   };
   ```

## New Data Structure

### Business Object (Updated):
```json
{
  "id": 1,
  "name": "Example Business",
  "phone": "(636) 555-0100",
  "contacts": [
    {
      "id": 1,
      "name": "John Smith",
      "title": "Manager",
      "phone": "(636) 555-0101",
      "email": "john@example.com",
      "notes": "Decision maker",
      "isPrimary": true
    }
  ],
  "visits": [
    {
      "date": "2026-01-03",
      "notes": "Regular visit notes",
      "duration": "30 min",
      "metWith": "John Smith",
      "activityType": "Sales Call",
      "opportunityNotes": "Follow up on Q1 order"
    }
  ]
}
```

## New UI Components

### 1. Business Card Scanner Button
- Located in business popup
- Opens camera/file upload modal
- Uses Tesseract.js to extract:
  - Name
  - Company name
  - Title/position
  - Phone number(s)
  - Email address
  - Physical address

### 2. Contacts Tab in Business Popup
- View all contacts for a business
- Add new contacts manually
- Edit existing contacts
- Set primary contact

### 3. Enhanced Visit Note Modal
- **Met With** dropdown (populated from business contacts)
- **Activity Type** selector:
  - Sales Call
  - Discovery Call
  - Product Demo
  - Account Review
  - Follow-up
  - Delivery
  - Service Call
  - Other
- **Opportunity Notes** field (for deals/follow-ups)
- Regular visit notes (still with voice input)

### 4. Voice Business Lookup
- During voice-guided entry
- Say business name
- System searches and shows suggestions
- Select match to auto-fill all details

### 5. Email Settings Panel
- Configure email report settings
- Test email functionality
- Set report time (default 5:30 PM CST)
- Enable/disable automatic reports

## Activity Types

The system tracks these activity types:
- **Sales Call** - Standard sales visit
- **Discovery Call** - Initial meeting/needs assessment
- **Product Demo** - Demonstrating products/services
- **Account Review** - Regular check-in with existing customer
- **Follow-up** - Following up on previous conversation
- **Delivery** - Delivering products/materials
- **Service Call** - Service or support visit
- **Other** - Any other type of interaction

## Daily Email Report Format

```
Daily Territory Report - January 3, 2026

VISITS TODAY: 3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Example Business Inc.
   St. Charles, MO (63301)
   Met with: John Smith
   Activity: Sales Call
   Duration: 45 min

   Notes: Discussed Q1 pricing strategy...

   OPPORTUNITY: Potential Q1 bulk order - 500 units
   ACTION: Follow up in 2 weeks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2. ABC Manufacturing
   St. Peters, MO (63376)
   Met with: Sarah Johnson
   Activity: Product Demo
   Duration: 60 min

   Notes: Demonstrated new product line...

   OPPORTUNITY: Interested in Q2 contract
   ACTION: Send proposal by Friday

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY:
- Total Visits: 3
- New Opportunities: 2
- Follow-up Actions: 2
```

## How to Use New Features

### Scan a Business Card:
1. Click on a business marker (or create new business)
2. In the popup, click "📷 Scan Business Card"
3. Take photo or upload image
4. Review extracted information
5. Click "Save Contact" to add to business

### Add Visit with Contact Tracking:
1. Click business marker
2. Click "🎤 Add Visit Note"
3. Select who you met with (dropdown)
4. Select activity type
5. Speak or type visit notes
6. Add opportunity notes if applicable
7. Click "Save Note"

### Use Business Lookup (Voice or Manual):

**Option 1: Voice Lookup**
1. Click "+ Add Business" button
2. Click "🎤 Voice Guide"
3. When prompted for business name, say the name
4. If business exists locally or in public database, you'll see suggestions
5. Click suggestion to auto-fill all fields
6. Or continue with new business entry

**Option 2: Manual Typed Search**
1. Click "+ Add Business" button
2. (Optional) Enter your current zip code in "Your Location Zip Code" field for better results
3. Type business name in the "Business Name" field (at least 3 characters)
4. Click "🔍 Search" button
5. Review suggestions from your database and public sources
6. Click a match to auto-fill all details
7. Or leave it blank and fill in manually

### View Daily Report:
- Reports automatically email at 5:30 PM CST
- Or click "📧 Send Daily Report Now" to test
- Check your Gmail inbox

## Technical Details

### Dependencies Added:
- **Tesseract.js** (CDN): OCR processing
- **EmailJS** (CDN): Email delivery service

### Browser Requirements:
- Chrome, Edge, or Safari (for camera access)
- Microphone access (for voice features)
- Modern JavaScript support (ES6+)

### Data Storage:
- All data stored in browser localStorage
- Export/import functionality available
- No photos stored (only extracted text data)

### Privacy & Security:
- Business card photos processed locally (not uploaded)
- Tesseract.js runs entirely in browser
- EmailJS uses secure HTTPS
- Email credentials not stored in code (configured once)

## Troubleshooting

### Business Card Scanner Not Working:
- Ensure browser supports camera API
- Grant camera permission when prompted
- Use well-lit, clear photo of card
- Try uploading instead of camera if issues persist

### Email Reports Not Sending:
- Verify EmailJS credentials are correct
- Check Email JS dashboard for quota (200/month free)
- Test with "Send Now" button first
- Check spam folder

### Business Lookup Not Finding Expected Results:

**Check the browser console (F12 → Console tab) to see debug information:**
- How many results OpenStreetMap returned
- What types of businesses were found
- Whether your zip code geocoded correctly

**Common Issues:**

1. **Business not in OpenStreetMap database:**
   - OpenStreetMap is community-maintained and may not have all businesses
   - Some newer or smaller businesses might not be listed yet
   - Try searching by business type instead (e.g., "restaurant", "coffee shop")
   - You can always add businesses manually

2. **Search term too generic:**
   - "Roadhouse" might return multiple results across Missouri
   - Try more specific: "Texas Roadhouse", "Logan's Roadhouse", etc.
   - Add location details: "Roadhouse 63385" or "Roadhouse Wentzville"

3. **Zip code not helping with location:**
   - Check console to verify zip code geocoded (look for "✅ Location from zip code")
   - Try different search terms
   - Leave zip code blank and try GPS instead (more accurate on mobile)

4. **Business classified differently:**
   - Restaurants might be under `amenity=restaurant` or `tourism`
   - The search now includes: shops, amenities, offices, tourism, leisure, restaurants, cafes, bars, pubs, hotels
   - If still not found, the business may not be in OpenStreetMap

**Workarounds:**
- Search by category: "steakhouse 63385" instead of specific name
- Add the business manually if not found
- Contribute to OpenStreetMap to add missing businesses (optional)

## Cost Information

All new features use FREE services:

- **Tesseract.js**: 100% free, open source
- **EmailJS Free Tier**: 200 emails/month (plenty for daily reports)
- **No API costs**: Everything runs in browser or uses free tiers

## Next Steps

1. Complete the EmailJS setup (see above)
2. Test business card scanner with a real card
3. Add a few visits to test email reports
4. Use "Send Now" button to verify email setup
5. Let automatic 5:30 PM emails handle the rest!

---

For questions or issues, refer to the main README.md or check browser console (F12) for error messages.
