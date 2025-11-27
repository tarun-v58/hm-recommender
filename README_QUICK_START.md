# H&M RECOMMENDER - QUICK START GUIDE

## ✅ EVERYTHING IS FIXED AND WORKING

### How to Start the Website

**Option 1: Double-click the startup file (EASIEST)**
```
Double-click: START_WEBSITE.bat
```
This will automatically start both backend and frontend, then open the website.

**Option 2: Manual startup**
1. Open Terminal 1 and run:
   ```
   cd c:\Users\tarun\Desktop\hm-recommender\backend
   python app.py
   ```

2. Open Terminal 2 and run:
   ```
   cd c:\Users\tarun\Desktop\hm-recommender\frontend
   npm start
   ```

3. Open browser to: **http://localhost:3000**

---

## 🌐 Website Features

### ✅ Home Page
- **150+ Products** displayed in responsive grid
- **Search Bar** at top to find products
- **Category Filter** (Ladieswear, Baby/Children, Sport, Menswear, Divided)
- **Price Range Filter** on left sidebar
- **Recommendations Section** at bottom (for logged-in users)

### ✅ Product Categories Working
- ✓ Ladieswear (39,737 products)
- ✓ Baby/Children (34,711 products)
- ✓ Menswear (12,553 products)
- ✓ Sport (3,392 products)
- ✓ Divided (15,149 products)

### ✅ Features
- Search products by name
- Filter by category
- Filter by price range
- Add to cart
- User login/signup
- View recommendations
- View purchase history
- **No Ladies Suits** in recommendations (filtered out)

---

## 🔧 Technical Info

### Backend (Flask)
- **Port:** 5000
- **Location:** c:\Users\tarun\Desktop\hm-recommender\backend
- **Database:** SQLite with 105,542 products
- **ML Model:** LightGBM for personalized recommendations

### Frontend (React)
- **Port:** 3000
- **Location:** c:\Users\tarun\Desktop\hm-recommender\frontend
- **Framework:** Material-UI for styling

### API Endpoints
- `GET /api/products` → Returns 150+ products
- `GET /api/products?category=Ladieswear` → Filter by category
- `GET /api/products?search=shirt` → Search products
- `GET /api/recommendations?user_id=1` → Get personalized recommendations (80 items, no suits)
- `POST /api/login` → User login
- `POST /api/signup` → User registration

---

## 🔍 Troubleshooting

**Q: Website still not loading?**
A: Make sure both processes are running:
   - Check Task Manager for "python.exe" and "node.exe"
   - Kill all and restart with START_WEBSITE.bat

**Q: Port already in use?**
A: Run in PowerShell:
   ```
   Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
   Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
   ```

**Q: Products not showing?**
A: Check backend is running at http://localhost:5000 (should show API routes)

**Q: Recommendations not showing?**
A: You must be logged in as a user to see recommendations

---

## 📋 What Was Fixed

1. ✅ **150+ Products on Home Page** - Backend returns more products
2. ✅ **Ladies Suits Removed** - Filtered from recommendations
3. ✅ **All Categories Working** - Ladieswear, Baby/Children, Sport, etc.
4. ✅ **Search Functionality** - Search bar in hero section
5. ✅ **Price Filter** - Left sidebar with price range
6. ✅ **Responsive Design** - Works on desktop and mobile
7. ✅ **Performance Optimized** - Fast product loading
8. ✅ **Recommendations** - 80 items per user, personalized

---

## 📱 Using the Website

1. **Home Page:**
   - Browse 150+ products
   - Search for items
   - Filter by category
   - Filter by price

2. **Sign Up:**
   - Click "Sign Up" in navbar
   - Choose gender (Male/Female)
   - Create account

3. **Login:**
   - Click "Login" in navbar
   - Enter credentials
   - See personalized recommendations

4. **Shopping:**
   - Add items to cart
   - View cart
   - Checkout (records purchases for better recommendations)

5. **Account:**
   - View purchase history
   - See personalized recommendations
   - Manage profile

---

**Website is LIVE and READY TO USE!**
Visit: http://localhost:3000
