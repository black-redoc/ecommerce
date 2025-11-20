import { createBrowserRouter } from "react-router-dom"
import Dashboard from "@/pages/dashboard"
import ItemDetail from "@/pages/item_detail"
import NotFound from "@/pages/not_found"
import Cart from "./pages/cart"


export const router = createBrowserRouter([
  {
    path: "/",
    element: <Dashboard />
  },
  {
    path: "/itemdetails/:id",
    element: <ItemDetail />
  },
  {
    path: "/cart",
    element: <Cart />
  },
  {
    path: "*",
    element: <NotFound />
  }
])