# H&M E-Commerce Recommender System

A full-stack e-commerce recommendation engine with a Flask backend and React+TypeScript frontend, featuring personalized product recommendations using LightGBM ML models and content-based filtering.

![Technologies](https://img.shields.io/badge/Flask-2.3.3-blue?style=flat&logo=flask)
![React](https://img.shields.io/badge/React-19.2.0-61dafb?style=flat&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178c6?style=flat&logo=typescript)
![Material-UI](https://img.shields.io/badge/Material--UI-7.3.4-007fff?style=flat&logo=mui)
![SQLite](https://img.shields.io/badge/SQLite-3-003b57?style=flat&logo=sqlite)

## Features

✨ **Smart Recommendations**
- Content-based recommendation engine using product similarity
- Different recommendations for each user based on purchase history
- ML-powered personalization with LightGBM
- Graceful fallbacks for new users

🛒 **E-Commerce Functionality**
- Browse 105,542 products across 5 categories
- Advanced filtering: search, category, gender, price range
- Shopping cart with per-user isolation
- Purchase history tracking
- Similar products suggestions

👤 **User Management**
- User authentication (login/signup)
- Gender-based product filtering
- Per-user cart persistence
- Purchase history and recommendations dashboard

📱 **Responsive Design**
- Mobile-first approach
- Desktop sidebar filters
- Mobile drawer navigation
- Material-UI components
- 150+ products displayed on home page

## Project Structure

```
hm-recommender/
├── backend/
│   ├── app.py                 # Flask REST API server
│   ├── models.py              # SQLAlchemy database models
│   ├── recommend.py           # Recommendation engine
│   ├── init_db.py             # Database initialization
│   ├── requirements.txt        # Python dependencies
│   ├── data/                  # CSV data files
│   ├── images/                # Product images (by folder)
│   ├── static/                # Placeholder images
│   └── hm_recommender.txt     # Pre-trained LightGBM model
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── contexts/          # React Context (Cart)
│   │   ├── services/          # API client
│   │   ├── App.tsx            # Main app component
│   │   └── index.tsx          # Entry point
│   ├── public/                # Static assets
│   ├── package.json           # Node dependencies
│   └── tsconfig.json          # TypeScript config
├── .gitignore                 # Git ignore rules
├── START.bat                  # One-click startup script
└── README.md                  # This file
```

## Getting Started

### Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 14+** & **npm** (for frontend)
- **Windows** (for START.bat script) or manual startup on other OS

### Quick Start (Windows)

Simply double-click `START.bat` to start both servers:
- Backend runs on `http://localhost:5000`
- Frontend runs on `http://localhost:3000`
- Browser opens automatically

### Manual Setup

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Start Flask server
python app.py
```

Backend will be available at `http://localhost:5000`

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will be available at `http://localhost:3000` and automatically opens in browser.

## API Documentation

### Authentication Endpoints

**POST** `/api/signup`
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "gender": "male" // or "female"
}
```

**POST** `/api/login`
```json
{
  "username": "john_doe",
  "password": "secure_password"
}
```
Returns: `{ user_id, username, gender }`

### Products Endpoints

**GET** `/api/products` - Get products with filters
- Query params: `category`, `search`, `gender`
- Returns: Array of products

**GET** `/api/products/<article_id>` - Get product details
- Returns: Product with `similar_products` array

**GET** `/api/categories` - Get all product categories
- Returns: Array of category names

### Recommendations Endpoint

**GET** `/api/recommendations?user_id=<id>` - Get personalized recommendations
- Returns: Array of recommended products (only for users with purchases/cart items)
- New users see no recommendations until they add items to cart

### Purchase Endpoints

**POST** `/api/buy` - Record a purchase
```json
{
  "user_id": 1,
  "article_id": 108775015
}
```

**GET** `/api/purchases?user_id=<id>` - Get purchase history
- Returns: Array of purchases with product details

## Features Deep Dive

### Recommendation System

The recommendation engine works in three tiers:

1. **Content-Based Filtering**: Analyzes products similar to user's purchases
2. **Fallback Strategy**: Uses popular items if model unavailable
3. **Gender Filtering**: Ensures recommendations match user preferences

**Smart Logic**:
- ✅ No recommendations for brand new users (no purchases/cart items)
- ✅ Recommendations update as user adds items to cart
- ✅ Different recommendations per user based on purchase history
- ✅ Excludes already-purchased and incompatible products

### Per-User Cart System

Each user has an isolated shopping cart:
- Stored in localStorage as `cart_user_${userId}`
- Persists across browser sessions
- Resets when user logs out
- Separate cart for each user account

### Product Database

- **105,542 total products** across 5 categories:
  - Ladieswear (39,737)
  - Menswear (12,553)
  - Baby/Children (34,711)
  - Sport (3,392)
  - Divided (15,149)

- **Images**: Stored in `/images/<folder>/<article_id>.jpg` structure
- **All products**: Fixed at $29.99 for demo purposes

## Frontend Components

| Component | Purpose |
|-----------|---------|
| `ProductList` | Browse 150+ products with filters |
| `ProductDetail` | View full product info and similar items |
| `Account` | Purchase history and recommendations |
| `Cart` | Shopping cart and checkout |
| `Login/Signup` | User authentication |
| `NavBar` | Navigation and user menu |
| `Recommendations` | Personalized product suggestions |

## Key Technologies

**Backend**:
- Flask 2.3.3 - Web framework
- SQLAlchemy 3.0.5 - ORM
- LightGBM 4.0.0 - ML model
- scikit-learn 1.3.0 - ML utilities
- Flask-CORS 4.0.0 - Cross-origin support

**Frontend**:
- React 19.2.0 - UI framework
- TypeScript 5.0 - Type safety
- Material-UI 7.3.4 - Component library
- Axios 1.12.2 - HTTP client
- React Router 7.9.4 - Navigation

**Database**:
- SQLite - Local database
- Alembic - Database migrations (if needed)

## Configuration

### Backend Settings

Edit `backend/app.py`:
- `SQLALCHEMY_DATABASE_URI` - Database path
- `debug=True` - Development mode

### Frontend Settings

Edit `frontend/package.json`:
- `proxy` - API backend URL (defaults to `http://localhost:5000`)

### Environment Variables

Create `.env` file in project root (optional):
```
FLASK_ENV=development
FLASK_DEBUG=true
NODE_ENV=development
```

## Database Schema

### Users Table
```sql
CREATE TABLE user (
  id INTEGER PRIMARY KEY,
  username VARCHAR UNIQUE NOT NULL,
  email VARCHAR UNIQUE,
  password_hash VARCHAR,
  gender VARCHAR CHECK(gender IN ('male', 'female'))
);
```

### Products Table
```sql
CREATE TABLE product (
  article_id INTEGER PRIMARY KEY,
  prod_name VARCHAR,
  product_type_name VARCHAR,
  colour_group_name VARCHAR,
  index_group_name VARCHAR,
  garment_group_name VARCHAR,
  detail_desc TEXT,
  image_path VARCHAR
);
```

### Purchases Table
```sql
CREATE TABLE purchase (
  id INTEGER PRIMARY KEY,
  user_id INTEGER FOREIGN KEY REFERENCES user(id),
  article_id INTEGER FOREIGN KEY REFERENCES product(article_id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Troubleshooting

### Backend Issues

**Port 5000 already in use**:
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F
```

**Database not initializing**:
```bash
# Delete existing database and reinitialize
rm backend/instance/shop.db
python backend/init_db.py
```

### Frontend Issues

**Port 3000 already in use**:
- Frontend will automatically prompt to use port 3001

**Npm dependencies not installing**:
```bash
# Clear npm cache
npm cache clean --force

# Reinstall
rm -rf node_modules package-lock.json
npm install
```

## Performance Optimizations

- ✅ **Lazy Loading**: Models load on first request
- ✅ **Caching**: Product features cached in memory
- ✅ **Pagination**: Returns 150+ products efficiently
- ✅ **Batch Similarity Calculation**: Memory-efficient product matching
- ✅ **Gender Filtering**: Server-side filtering reduces payload

## Security Notes

- ⚠️ Passwords hashed with werkzeug security
- ⚠️ CORS enabled for development (restrict in production)
- ⚠️ Use environment variables for sensitive data
- ⚠️ Implement rate limiting for production
- ⚠️ Add HTTPS/SSL in production

## Future Enhancements

- [ ] User reviews and ratings
- [ ] Wishlist/favorites system
- [ ] Real-time inventory management
- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] Advanced analytics dashboard
- [ ] Recommendation A/B testing
- [ ] Email notifications
- [ ] Mobile app (React Native)
- [ ] Docker containerization
- [ ] CI/CD pipeline

## Development Workflow

1. **Create feature branch**:
   ```bash
   git checkout -b feature/feature-name
   ```

2. **Make changes** and commit:
   ```bash
   git add .
   git commit -m "Add feature description"
   ```

3. **Push to GitHub**:
   ```bash
   git push origin feature/feature-name
   ```

4. **Create Pull Request** on GitHub

## Building for Production

### Backend

```bash
# Install production dependencies
pip install -r requirements.txt

# Use WSGI server (e.g., Gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend

```bash
# Create optimized production build
npm run build

# Output in `build/` folder
# Deploy to CDN or web server
```

## Testing

Run unit tests:
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Contact & Support

- **GitHub Issues**: Report bugs and request features
- **Email**: tarun@example.com
- **Documentation**: Check `/docs` folder

## Acknowledgments

- H&M Dataset for product data
- LightGBM for ML model
- Material-UI for beautiful components
- Open-source community

---

**Last Updated**: November 2025
**Version**: 1.0.0
