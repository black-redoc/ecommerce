import Navbar from "@/components/navbar"
import Products from "@/components/products"

const Dashboard = () => {
  return (
    <main className="mt-12 place-content-center flex w-screen">
      <Navbar/>
      <Products />
    </main>
  )
}

export default Dashboard