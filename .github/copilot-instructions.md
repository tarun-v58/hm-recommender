# H&M Recommender AI Coding Assistant Instructions

## Project Overview
H&M Recommender is a full-stack e-commerce recommendation engine with a Flask backend and React+TypeScript frontend. The system personalizes product recommendations using LightGBM ML models, gender-based filtering, and similarity scoring.

## Architecture

### Backend (Flask + SQLAlchemy)
- **Entry point**: `backend/app.py` - Flask REST API with auth, products, purchases, and recommendations endpoints
- **Data models**: `backend/models.py` - Three tables: `User` (with gender), `Product` (article catalog), `Purchase` (transaction history)
- **Recommendations engine**: `backend/recommend.py` - Lazy-loads LightGBM model; provides personalized recs and similar products via cosine similarity
- **Database setup**: `backend/init_db.py` - Loads products from CSV, maps images from `/images/<folder>/<article_id>.jpg` structure
- **Dependencies**: Flask 2.3.3, SQLAlchemy 3.0.5, LightGBM 4.0.0, scikit-learn 1.3.0

### Frontend (React + TypeScript + Material-UI)
- **Entry point**: `frontend/src/App.tsx` - Router with routes for products, login/signup, cart, account, recommendations
- **API client**: `frontend/src/services/api.ts` - Axios wrapper; all backend calls proxied to `http://localhost:5000` (see `package.json` proxy)
- **State management**: `frontend/src/contexts/CartContext.tsx` - React Context for shopping cart (persisted to localStorage)
- **Components**: In `frontend/src/components/` - ProductList, ProductDetail, Recommendations, Login, Signup, Account, Cart, NavBar, GridItem
- **Theme**: Material-UI custom theme with H&M brand colors (dark #1a1a1a, red #e60012)

### Data Flow
1. User authenticates via `/api/signup` or `/api/login` (stores `user_id`, `username`, `gender` in localStorage)
2. Frontend fetches `/api/products` with optional `category`, `search`, and `gender` filters
3. For logged-in users: `/api/recommendations?user_id=<id>` returns personalized list, gender-filtered
4. Purchase tracking: `/api/buy` records transaction; `/api/purchases?user_id=<id>` retrieves history
5. Product similarity: `/api/products/<article_id>` includes `similar_products` IDs for related items

## Key Patterns & Conventions

### Gender-Based Filtering (Recurring Pattern)
**Why**: Ensure recommendations and product listings match user's declared gender preference.

**Implementation**: Both `app.py` and `recommend.py` use identical filtering logic:
```python
# Check for gender terms in index_group_name or garment_group_name
is_male_product = any(term in category_string.lower() for term in ['men', 'boy', 'male'])
is_female_product = any(term in category_string.lower() for term in ['women', 'girl', 'lady', 'female'])
```
- Applied in: `app.py` (products endpoint, recommendations endpoint), `recommend.py` (get_personalized_recommendations)
- Unisex products (no gender terms) are included for both genders
- **When modifying**: Keep filtering logic in sync across both files to prevent inconsistent results

### Fallback & Error Handling in Recommendations
**Pattern**: Multi-tier fallback for robustness when ML model unavailable.
1. Try loading LightGBM model (`recommend.py._load_model()` - lazy loaded once)
2. If model fails: use simple recency scoring (fall back to `scores = [f[0] for f in features]`)
3. If no purchases: return popular gender-appropriate products (first 50)
4. Always validate recommendations against user's gender before returning

**Rationale**: Model file (`hm_recommender.txt`) may be missing or corrupted; system should gracefully degrade rather than crash.

### Image Path Resolution
**Pattern**: Images stored as `/images/<folder>/<article_id>.jpg` where folder is zero-padded (010-095).

- `init_db.py.find_image_path()` searches for image during DB initialization
- Image endpoints: Flask routes `/images/<path:filename>` and `/static/<path:filename>` with fallback to placeholder
- Store relative path in DB (e.g., `"010/010875015.jpg"`) for portability

### Lazy Loading & Caching (recommend.py)
- `_model`, `_model_load_error`, `_product_features_df` are module-level caches
- `_load_model()` called once; subsequent calls are no-ops
- `get_product_features()` computes DataFrame on first call, then caches
- Features are hashed attributes: `product_type_no`, `colour_group_code`, `index_group_no`, `garment_group_no`

**When modifying**: Do not reset caches unless explicitly needed; lazy loading avoids expensive operations on each request.

### Frontend-Backend Communication
- All API calls from `frontend/src/services/api.ts`; all use `/api/` prefix
- `package.json` proxy routes requests to Flask backend (port 5000)
- User ID stored in localStorage after login; passed as URL param or JSON body
- Responses validated in frontend API layer to catch malformed data early

### Database Context Requirement
`get_product_features()` and all functions accessing SQLAlchemy models require Flask app context.
- Called only within request handlers or wrapped in `with app.app_context():`
- Example: `init_db.py` uses `with app.app_context(): load_products()`

## Common Workflows

### Adding a New Recommendation Strategy
1. Add logic to `backend/recommend.py:get_personalized_recommendations()`
2. Ensure gender filtering is applied before returning products
3. Test with both new and returning users
4. If using model prediction: handle `_model is None` case with fallback scoring

### Adding a New Product Filter
1. Update `/api/products` endpoint in `app.py` to accept new query param
2. Apply `get_gender_filter()` to maintain gender consistency
3. Update frontend `api.ts` call signature and `ProductList.tsx` to pass parameter

### Displaying Products in Frontend
- Use `GridItem.tsx` component to render individual products with image, name, price
- Images loaded from `/images/` endpoint (Flask serves from `backend/images/`)
- Handle missing images gracefully (Flask returns placeholder.jpg)

### Managing Cart State
- CartContext holds array of `CartItem` (Product + quantity)
- Changes automatically persisted to localStorage via `useEffect`
- Components import `useCart()` hook to access cart functions
- Cart total computed client-side: `sum(item.price * item.quantity)`

## Development Commands (Backend)
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database (one-time, will drop/recreate tables)
python init_db.py

# Run Flask dev server (default http://localhost:5000)
python app.py
```

## Development Commands (Frontend)
```bash
# Install dependencies
npm install

# Start dev server (http://localhost:3000, proxies API to :5000)
npm start

# Build for production
npm build
```

## Testing & Debugging
- Flask debug mode enabled by default: changes auto-reload
- Frontend React hot-reload works with edits to `.tsx` files
- Check browser console for frontend errors; Flask console for backend
- Verify database state: query `backend/instance/shop.db` (SQLite)
- Model status endpoint: `GET /status` returns `{model: {loaded, error}, product_count}`

## Important Notes
- **Fixed price**: All products return `price: 29.99` (hardcoded for now)
- **Database reset**: `init_db.py` drops all tables each time; use cautiously in production
- **CORS enabled**: Frontend can access backend from different origin
- **Image folder range**: Currently supports articles in folders 010-095; adding more requires updating `init_db.py` range
