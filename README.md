# Missouri Territory Map - Complete User Guide

Welcome to your interactive territory map! This guide will help you use and maintain your map.

## 🚀 Quick Start - How to Open Your Map

### IMPORTANT: Use the Local Server
The map needs to run on a local web server to work properly. Here's how:

1. **Open Terminal** (on Mac: Applications → Utilities → Terminal)
2. **Navigate to your project folder**:
   ```bash
   cd /Users/joelcochrane/Code/first-project
   ```
3. **Start the server**:
   ```bash
   python3 -m http.server 8000
   ```
4. **Open your browser** and go to:
   ```
   http://localhost:8000
   ```
5. **Keep the Terminal window open** while using the map. When you're done, press `Ctrl+C` in Terminal to stop the server.

### Alternative: Quick Server Start
If the server is already running, just go to [http://localhost:8000](http://localhost:8000) in your browser.

---

## ✅ What Your Map Can Do (All Phases Complete!)

### Territory Visualization
- ✅ Interactive map centered on your Missouri territory
- ✅ Colored zip code boundaries for your 4 territories:
  - **63301** - St. Charles (Red)
  - **63376** - St. Peters (Blue)
  - **63368** - O'Fallon (Green)
  - **63385** - Winfield (Purple)
- ✅ Legend showing what each color means
- ✅ Click any zip code to see details
- ✅ Hover over boundaries to highlight them

### Business Tracking & CRM Features
- ✅ **Smart Business Markers** with visual indicators:
  - **Green pins** = Existing customers
  - **Blue pins** = Prospective customers
  - **Pin size** indicates activity level (bigger = more interactions)
  - **Red badge with number** = 6+ interactions
  - **Star icon** = High priority customers

- ✅ **Click any business marker** to see:
  - Full business details and address
  - Customer status badge
  - Total interaction count
  - Last visit date
  - Recent visit history with notes
  - Action buttons

- ✅ **Toggle Customer Status**: Switch between existing/prospective with one click

### Voice Input for Visit Documentation
- ✅ **Hands-free documentation** using your computer's microphone
- ✅ Click "🎤 Add Visit Note" on any business
- ✅ Speak naturally - it transcribes in real-time
- ✅ Edit transcription before saving if needed
- ✅ Automatic timestamp recording
- ✅ All notes saved to business history
- ✅ **Works in**: Chrome, Edge, Safari (iOS 14.5+)

### Search & Filter Features
- ✅ **Real-time search** across:
  - Business names
  - Addresses and cities
  - Zip codes
  - Visit notes and conversation history

- ✅ **Filter by Customer Status**:
  - Show/hide existing customers
  - Show/hide prospective customers

- ✅ **Filter by Activity Level**:
  - High Activity (6+ visits)
  - Medium Activity (3-5 visits)
  - Low Activity (1-2 visits)

- ✅ **Filter by Priority**:
  - Show only high priority customers

- ✅ **Map Display Controls**:
  - Toggle zip code boundaries on/off
  - Toggle business markers on/off

- ✅ **Clear All Filters** button to reset everything

### Data Persistence
- ✅ All changes saved automatically in your browser
- ✅ Visit notes persist between sessions
- ✅ Customer status changes saved
- ✅ Works offline after initial load

---

## 📖 How to Use Your Map

### Basic Navigation
- **Click and drag** to move around the map
- **Mouse wheel** or **+/- buttons** to zoom in and out
- **Double-click** anywhere to zoom in quickly

### Finding Businesses

**Option 1: Visual Search**
- Look at the colored pins on the map
- Green = existing customers, Blue = prospective
- Larger pins = more active customers
- Stars = high priority

**Option 2: Use the Search Box**
1. Look for the "Search & Filter" panel on the left
2. Type in the search box (business name, address, city, zip, or keywords from visit notes)
3. Results update in real-time as you type
4. The map shows only matching businesses

**Option 3: Use Filters**
1. In the Search & Filter panel, check/uncheck filter options
2. For example:
   - Uncheck "Prospective Customers" to see only existing customers
   - Check "High Priority Only" to see just your priority accounts
   - Uncheck "Low Activity" to focus on active accounts

### Documenting a Visit

**The Easy Way (Voice Input):**
1. Click on a business marker on the map
2. In the popup, click "🎤 Add Visit Note"
3. A modal window opens
4. Click the microphone button (it turns red)
5. Speak your visit notes naturally:
   - "Met with John Smith. Discussed Q1 order for 500 units. They're interested in our new product line. Follow up next Tuesday."
6. Click the microphone again to pause (or keep speaking)
7. Review the transcription (you can edit it by clicking in the text area)
8. Click "Save Note"
9. Done! The visit is recorded with today's date and time

**Manual Entry:**
- Follow the same steps, but instead of using the microphone, just type directly in the text area

### Changing Customer Status
1. Click on a business marker
2. In the popup, click "Toggle Status"
3. The customer switches between "existing" and "prospective"
4. The marker color changes automatically (green ↔ blue)
5. Changes are saved immediately

### Viewing Visit History
1. Click on any business marker
2. Scroll down in the popup to see "Recent Visits"
3. See the 3 most recent visits with:
   - Date
   - Duration
   - Full notes from each visit

---

## 🎨 Understanding the Visual Indicators

### Pin Colors
- **Green** = Existing customer
- **Blue** = Prospective customer

### Pin Sizes
- **Small** = 1-2 interactions
- **Medium** = 3-5 interactions
- **Large with red badge** = 6+ interactions (shows number)

### Special Markers
- **⭐ Star** = High priority customer (top-left of pin)
- **Red number badge** = Exact interaction count for very active accounts

### Zip Code Boundaries
- **Red** = St. Charles (63301)
- **Blue** = St. Peters (63376)
- **Green** = O'Fallon (63368)
- **Purple** = Winfield (63385)

---

## 🔧 Managing Your Data

### Where is Data Stored?
- **Original data**: `data/businesses.json` file
- **Updates and changes**: Saved in your browser's localStorage
- **This means**: Your changes persist on your computer but won't automatically sync to other devices

### Adding New Businesses
1. Open `data/businesses.json` in any text editor
2. Copy an existing business entry
3. Paste it and modify the details:
   ```json
   {
     "id": 4,
     "name": "New Business Name",
     "address": "456 Oak Street",
     "city": "St. Charles",
     "zipCode": "63301",
     "lat": 38.7881,
     "lng": -90.4974,
     "type": "Retail",
     "customerStatus": "prospective",
     "interactionCount": 0,
     "lastVisit": null,
     "priority": "medium",
     "visits": []
   }
   ```
4. **Finding coordinates (lat/lng)**:
   - Go to [Google Maps](https://maps.google.com)
   - Search for the address
   - Right-click on the exact location
   - Click the coordinates that appear (they'll copy automatically)
   - Paste into your JSON file
5. Save the file and refresh your browser

### Changing Zip Code Colors
1. Open `data/territory.json`
2. Change the color hex codes:
   ```json
   "63301": { "color": "#e41a1c", "name": "St. Charles" }
   ```
3. Use any hex color code (Google "color picker" for options)
4. Save and refresh

### Adding More Zip Codes to Your Territory
1. Open `data/territory.json`
2. Add a new entry:
   ```json
   "63304": { "color": "#ff9900", "name": "St. Charles West", "description": "West St. Charles area" }
   ```
3. Save and refresh
4. The boundary will automatically appear if it's in the Missouri GeoJSON file

---

## 🐛 Troubleshooting

### Map doesn't load or shows circles instead of boundaries

**Problem**: You opened the file directly (double-clicked index.html)

**Solution**: Must use the local server
1. Open Terminal
2. `cd /Users/joelcochrane/Code/first-project`
3. `python3 -m http.server 8000`
4. Go to `http://localhost:8000` in your browser

### Voice input doesn't work

**Problem**: Browser doesn't support Web Speech API

**Solutions**:
- ✅ **Use Chrome** (best support)
- ✅ **Use Edge** (also excellent)
- ✅ **Use Safari** (works well on Mac)
- ❌ Firefox has limited support

**Problem**: Microphone permission denied

**Solution**:
1. Click the 🔒 lock icon in your browser's address bar
2. Allow microphone access
3. Refresh the page

### Businesses don't appear

**Check**:
1. Is the server running? (Terminal should show "Serving HTTP")
2. Did you go to `localhost:8000` (not just opening the file)?
3. Open browser console (press F12) - any error messages?
4. Check that `data/businesses.json` exists and has valid JSON

### Changes aren't saving

**Likely cause**: Data is in localStorage, which is browser-specific

**Note**: Each browser stores data separately. If you switch browsers, you won't see your updates. Always use the same browser.

### Search isn't finding a business

**Check**:
- Is there a typo in your search?
- Are your filters excluding it? (Click "Clear All Filters")
- Try searching for just part of the name

---

## 🌐 Which Browser to Use?

### Recommended: Google Chrome
- ✅ All features work perfectly
- ✅ Best voice recognition
- ✅ Fastest performance
- ✅ Best developer tools if you need to troubleshoot

### Also Great: Microsoft Edge
- ✅ Same engine as Chrome
- ✅ Voice recognition works great
- ✅ All features supported

### Works Well: Safari (Mac)
- ✅ Map works perfectly
- ✅ Voice input supported (iOS 14.5+)
- ⚠️ Slightly slower performance

### Limited: Firefox
- ✅ Map works great
- ❌ Voice input has limited support
- ⚠️ May need to enable some permissions

---

## 💡 Tips & Best Practices

### For Best Voice Recognition
1. Use a good quality microphone (built-in Mac mic works well)
2. Speak clearly and at normal pace
3. Minimize background noise
4. Pause briefly between sentences
5. Review and edit transcription before saving

### Organizing Your Territory
- Use the **High Priority** checkbox to mark your key accounts
- Use **search** to quickly find businesses before a visit
- Filter by **activity level** to find accounts that need attention
- Filter by **prospective** to focus on conversion opportunities

### Regular Maintenance
- Add visit notes immediately after each visit while details are fresh
- Update customer status when prospects convert
- Review "Low Activity" filter monthly to identify neglected accounts
- Check high priority accounts weekly

---

## 📱 Mobile Use

The map is responsive and works on tablets and phones, but with some limitations:

**What Works**:
- ✅ Viewing the map
- ✅ Clicking markers
- ✅ Basic navigation
- ✅ Voice input (on mobile Safari and Chrome)

**What's Limited**:
- ⚠️ Small screen makes search panel harder to use (it's collapsible - click the − button)
- ⚠️ Adding/editing data is easier on desktop

**Tip**: Use mobile for field visits (voice notes), use desktop for data management

---

## 🔐 Data Privacy & Security

- ✅ All data stays on your computer (no cloud storage)
- ✅ Voice input processed locally by your browser (not sent to external servers)
- ✅ No login required, no accounts created
- ✅ No tracking or analytics
- ⚠️ Data is not encrypted (don't store sensitive passwords or credit card info)
- ⚠️ Browser localStorage can be cleared (export important data regularly - coming soon)

---

## 🚀 Future Enhancements (Optional)

Possible features we could add later:
- Export data to CSV or JSON file
- Import businesses from spreadsheet
- Print/PDF export for reports
- Route planning between multiple businesses
- Calendar integration for scheduled visits
- Photo attachments to visit notes
- Analytics dashboard (conversion rates, visits per zip code, etc.)

---

## 📞 Need Help?

If you run into issues or want to add features:
1. Check this README first
2. Look at the Troubleshooting section
3. Check browser console (F12) for error messages
4. Ask for help with specific error messages

---

## 📂 File Structure

Your project folder contains:
```
/Users/joelcochrane/Code/first-project/
├── index.html              # Main application (open in browser)
├── README.md               # This file
├── .gitignore              # Git configuration
└── data/
    ├── territory.json      # Your zip codes and colors (edit this)
    ├── mo-zipcodes.geojson # Missouri boundaries (download separately)
    └── businesses.json     # Your businesses (edit to add new ones)
```

**Files you can edit**:
- ✅ `data/territory.json` - to change colors or add zip codes
- ✅ `data/businesses.json` - to add new businesses
- ⚠️ `index.html` - advanced users only

**Files you shouldn't edit**:
- ❌ `data/mo-zipcodes.geojson` - large file with boundary data

### 📥 First-Time Setup: Download Missouri Boundary Data

**IMPORTANT**: If you're setting up this project for the first time (or cloning from GitHub), you need to download the Missouri zip code boundaries file:

1. **Download the file**:
   ```bash
   curl -L "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/mo_missouri_zip_codes_geo.min.json" -o data/mo-zipcodes.geojson
   ```

2. **Or download manually**:
   - Go to: https://github.com/OpenDataDE/State-zip-code-GeoJSON
   - Download `mo_missouri_zip_codes_geo.min.json`
   - Save it as `mo-zipcodes.geojson` in the `data/` folder

**Why?** This file is 34.7MB and too large to include in the GitHub repository, so you'll need to download it separately.

---

**Version**: Complete - All Phases (1-6)
**Last Updated**: January 2026
**Status**: ✅ Production Ready
