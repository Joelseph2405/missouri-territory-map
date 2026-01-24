# Database Schema

## Tables

### businesses
Primary table storing business entities.
- `id` (Integer, Primary Key)
- `name` (Text)
- `address` (Text)
- `city` (Text)
- `zipCode` (Text)
- `lat` (Real)
- `lng` (Real)
- `type` (Text) - Industry/Category
- `customerStatus` (Text) - 'existing' or 'prospective'
- `interactionCount` (Integer)
- `lastVisit` (Text) - ISO Date string
- `priority` (Text) - 'high', 'medium', 'low'
- `phone` (Text)
- `contacts` (Text) - JSON String (LEGACY - Moving to `contacts` table)
- `visits` (Text) - JSON String (Array of visit objects)

### contacts
**NEW**: Stores individual contacts linked to businesses.
- `id` (Integer, Primary Key)
- `business_id` (Integer, Foreign Key -> businesses.id)
- `name` (Text)
- `title` (Text)
- `phone` (Text)
- `email` (Text)
- `notes` (Text)
- `created_at` (Text) - ISO Timestamp

### reminders
**NEW**: Stores follow-up reminders.
- `id` (Integer, Primary Key)
- `business_id` (Integer, Foreign Key -> businesses.id)
- `contact_id` (Integer, Foreign Key -> contacts.id, Nullable)
- `due_date` (Text) - YYYY-MM-DD
- `note` (Text)
- `status` (Text) - 'pending', 'completed', 'snoozed'
- `created_at` (Text) - ISO Timestamp
