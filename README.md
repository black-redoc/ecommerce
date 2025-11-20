# E-Commerce Shopping Cart

A modern, full-stack e-commerce shopping cart application built with React, TypeScript, and FastAPI. This project demonstrates a clean architecture with a responsive frontend and a RESTful backend API.

## Overview

This is a monorepo containing both frontend and backend applications for a complete e-commerce shopping cart system. The application allows users to browse products, view detailed product information, add items to their cart, and manage their shopping cart with real-time total calculations.

### Key Features

- **Product Catalog**: Browse products with images, names, prices, and ratings
- **Product Details**: View individual product pages with detailed information
- **Shopping Cart**: Add/remove items with automatic total calculation
- **Real-time Updates**: Cart count badge updates instantly
- **Responsive Design**: Mobile-first UI with Tailwind CSS
- **Type Safety**: Full TypeScript implementation
- **State Management**: Zustand for efficient, reactive state management
- **RESTful API**: FastAPI backend with async support
- **Database**: SQLAlchemy ORM with SQLite (easily adaptable to PostgreSQL/MySQL)

## Tech Stack

### Frontend
- **React** 19.2.0 - Modern UI framework
- **TypeScript** 5.9.3 - Type-safe JavaScript
- **React Router** 7.9.6 - Client-side routing
- **Zustand** 5.0.8 - Lightweight state management
- **Tailwind CSS** 4.1.17 - Utility-first CSS framework
- **Vite** 7.2.2 - Lightning-fast build tool

### Backend
- **FastAPI** 0.121.3+ - Modern Python web framework
- **SQLAlchemy** 2.0.44 - Async ORM
- **aiosqlite** 0.21.0 - Async SQLite driver
- **Uvicorn** 0.38.0 - ASGI server
- **Pydantic** - Data validation (included with FastAPI)
- **Python** 3.12+

## Project Structure

```
ecommerce_cart/
    frontend/                    # React TypeScript application
       src/
          main.tsx            # Application entry point
          App.tsx             # Root component
          routes.tsx          # Route definitions

          pages/              # Page components
           dashboard.tsx   # Home page with product grid
           item_detail.tsx # Product detail page
           cart.tsx        # Shopping cart page
           not_found.tsx   # 404 error page

          components/         # Reusable UI components
           navbar.tsx      # Navigation header
           products.tsx    # Product grid component
           icons/          # SVG icon components

          store/              # Zustand state management
            item_store.ts   # Products state
            cart_store.ts   # Shopping cart state

          domain/types/       # TypeScript type definitions
            item_type.ts    # Product type
            cart_type.ts    # Cart type
            item_response_type.ts # API response type

          hooks/              # Custom React hooks
                   useloaditem.tsx # Product loading hook

        package.json            # Dependencies and scripts
        vite.config.ts          # Vite configuration
        tsconfig.json           # TypeScript configuration
        tailwind.config.js      # Tailwind CSS configuration
```

## Architecture

### Frontend Architecture

The frontend follows a modern React architecture with clear separation of concerns:

1. **Pages Layer**: Top-level route components ([pages/](src/pages/))
2. **Components Layer**: Reusable UI components ([components/](src/components/))
3. **State Management**: Zustand stores for global state ([store/](src/store/))
4. **Type Definitions**: TypeScript interfaces and types ([domain/types/](src/domain/types/))
5. **Custom Hooks**: Reusable logic encapsulation ([hooks/](src/hooks/))

### Backend Architecture

The backend uses a layered architecture pattern:

1. **Routes Layer**: HTTP request/response handlers ([routes/](../backend/routes/))
2. **Services Layer**: Business logic and database operations ([services/](../backend/services/))
3. **Models Layer**: Database schemas and validation ([models/](../backend/models/))
4. **Configuration Layer**: Database and settings management ([conf/](../backend/conf/))

### Data Flow

```
User Action | React Component | Zustand Store | UI Update
                                      |
                                 HTTP Request
                                      |
                            FastAPI Route Handler
                                      |
                              Service Layer
                                      |
                            SQLAlchemy ORM
                                      |
                              SQLite Database
```

## Getting Started

### Prerequisites

- **Node.js** 18+ and npm (for frontend)
- **Python** 3.12+ (for backend)
- **uv** (recommended) or pip for Python package management

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and install dependencies:
```bash
# Using uv (recommended)
uv sync

# Or using pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file:
```env
DATABASE_URL=sqlite+aiosqlite:///./db.sqlite3
IS_DEV=True
```

4. (Optional) Seed the database with sample data:
```bash
python seed.py
```

5. Start the backend server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Running Both Servers

Open two terminal windows:

**Terminal 1 (Backend):**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Items (Products)

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/item/` | List all products (paginated) | `{page: number, data: Item[]}` |
| GET | `/item/{id}` | Get product by ID | `Item` |
| POST | `/item/` | Create new product | `Item` |
| PUT | `/item/{id}` | Update product | `Item` |
| PATCH | `/item/{id}` | Partial update product | `Item` |

#### Carts

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/cart/` | List all carts | `Cart[]` |
| GET | `/cart/{id}` | Get cart by ID | `Cart` |
| POST | `/cart/` | Create new cart | `Cart` |
| PUT | `/cart/{id}` | Update cart items | `Cart` |
| DELETE | `/cart/{id}` | Delete cart | `{detail: string}` |

#### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/healthcheck` | API health status |

### Data Models

#### Item (Product)
```typescript
{
  id: number;
  name: string;
  value: number;
  image_url?: string;
}
```

#### Cart
```typescript
{
  id: number;
  items: Item[];
  total: number;
  count: number;
}
```

### Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Features in Detail

### State Management

The application uses Zustand for lightweight, efficient state management:

#### Item Store ([src/store/item_store.ts](src/store/item_store.ts))
- Manages the product catalog
- Handles loading states and errors
- Fetches products from the backend API

#### Cart Store ([src/store/cart_store.ts](src/store/cart_store.ts))
- Manages shopping cart items
- Automatically calculates total price
- Tracks item count for the cart badge
- Prevents duplicate items

### Routing

The application uses React Router v7 with the following routes:

- `/` - Dashboard (product listing)
- `/itemdetails/:id` - Product detail page
- `/cart` - Shopping cart
- `*` - 404 Not Found page

Routes are defined in [src/routes.tsx](src/routes.tsx).

### Custom Hooks

#### useLoadItemEffect ([src/hooks/useloaditem.tsx](src/hooks/useloaditem.tsx))
- Fetches products from the backend on mount
- Prevents duplicate requests
- Handles loading states and errors
- Updates the item store with fetched data

### Components

#### Navbar ([src/components/navbar.tsx](src/components/navbar.tsx))
- Fixed header with navigation
- Home button
- Cart button with item count badge
- Responsive design

#### Products ([src/components/products.tsx](src/components/products.tsx))
- Grid layout of product cards
- Fetches and displays products from API
- Responsive grid (adjusts to screen size)

## Development

### Available Scripts

#### Frontend
```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run lint     # Run ESLint
npm run preview  # Preview production build
```

#### Backend
```bash
uvicorn main:app --reload              # Development server
uvicorn main:app --host 0.0.0.0 --port 8000  # Production server
```

### Code Quality

#### Frontend
- **ESLint**: Configured for React, TypeScript, and React Hooks
- **TypeScript**: Strict mode enabled with comprehensive type checking
- **Vite**: Fast HMR (Hot Module Replacement) for development

#### Backend
- **Type Hints**: Full type annotations using Python 3.12+ syntax
- **Async/Await**: Non-blocking I/O throughout
- **Pydantic**: Runtime validation for all API requests/responses

## Database Schema

The backend uses a many-to-many relationship design:

```sql
-- Items (Products)
CREATE TABLE items (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  value REAL NOT NULL,
  image_url TEXT
);

-- Carts
CREATE TABLE carts (
  id INTEGER PRIMARY KEY
);

-- Many-to-Many Association
CREATE TABLE item_cart (
  item_id INTEGER REFERENCES items(id),
  cart_id INTEGER REFERENCES carts(id),
  PRIMARY KEY (item_id, cart_id)
);
```

## Configuration

### Frontend Configuration

#### Vite ([vite.config.ts](vite.config.ts))
- React plugin for JSX support
- Tailwind CSS plugin
- Path alias: `@` � `./src`

#### TypeScript ([tsconfig.json](tsconfig.json))
- Target: ES2022
- Strict mode enabled
- Path mapping for `@/*` imports

### Backend Configuration

#### Database ([backend/conf/database.py](../backend/conf/database.py))
- Async SQLAlchemy engine
- Session factory with dependency injection
- Automatic table creation on startup

#### CORS ([backend/main.py](../backend/main.py))
- Allows requests from `localhost:5173` (Vite dev server)
- Configured for all common HTTP methods
- Proper headers for authentication and content types

## Deployment

### Frontend Deployment

Build the frontend for production:
```bash
npm run build
```

The built files will be in the `dist/` directory. Deploy to:
- **Vercel** (recommended for React apps)
- **Netlify**
- **GitHub Pages**
- Any static hosting service

### Backend Deployment

The backend can be deployed to:
- **Railway**
- **Render**
- **Heroku**
- **AWS EC2**
- **Docker** (containerized deployment)

For production, consider:
- Using PostgreSQL instead of SQLite
- Setting up environment variables securely
- Enabling HTTPS
- Adding authentication/authorization
- Implementing rate limiting

## Future Enhancements

Potential improvements for this project:

### Frontend
- [ ] User authentication and login
- [ ] Product search and filtering
- [ ] Product categories/tags
- [ ] Wishlist functionality
- [ ] Order history
- [ ] Product reviews and ratings
- [ ] Checkout flow
- [ ] Payment integration
- [ ] Dark mode toggle

### Backend
- [ ] User authentication (JWT)
- [ ] Cart ownership (user-specific carts)
- [ ] Item quantity in cart (not just presence)
- [ ] Inventory management
- [ ] Order processing
- [ ] Payment processing
- [ ] Email notifications
- [ ] Product images upload
- [ ] Search API with filters
- [ ] Admin dashboard API

### DevOps
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Automated testing (unit, integration, e2e)
- [ ] Monitoring and logging
- [ ] Database migrations
- [ ] API rate limiting

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue in the repository.

---

**Built with modern web technologies and best practices.**
