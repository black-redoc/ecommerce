import CartIcon from "./icons/cart";
import { useNavigate } from "react-router-dom";
import { useCartStore } from "@/store/cart_store";

const Navbar = () => {
  const { data: cart } = useCartStore((state) => state)
  const navigate = useNavigate()
  const go_to_cart = () => {
    return navigate("/cart")
  }

  const go_to_home = () => {
    return navigate("/")
  }
  return (
    <nav className="bg-black w-full h-10 fixed top-0 left-0 flex place-items-center justify-between px-5 md:px-40 gap-24">
      <h1 className="font-bold">e-commerce</h1>
      <div className="flex gap-5">
        <button className="cursor-pointer hover:scale-101 transition-all hover:text-gray-50" onClick={go_to_home}>Inicio</button>
        <button className="cursor-pointer hover:scale-105 hover:text-gray-200 transitio-all bg-gray-700 rounded-4xl p-1 flex place-items-center place-content-center relative" onClick={go_to_cart}>
          <CartIcon />
          <p className="bg-red-400 font-bold rounded-4xl w-4 h-4 flex place-items-center place-content-center text-xs absolute top-0 left-6">
            {cart.count}
          </p>
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
