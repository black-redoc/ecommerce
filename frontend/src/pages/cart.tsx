import Navbar from "@/components/navbar"
import { useCartStore } from "@/store/cart_store"
import CruiseIcon from "@/components/icons/cruise"
import type { Item } from "@/domain/types/item_type"

const Cart = () => {
  const { data: cart_items, delete_item: delete_item_from_store } = useCartStore((state) => state)
  const delete_item = ({item}: {item: Item}) => {
    delete_item_from_store(item)
  }
  return <main className="mt-12 px-2 sm:px-0 w-screen">
    <Navbar />
    <div className="flex justify-between px-10 sm:px-40 border-b-2 border-gray-500 mb-5">
      <h1 className="text-black font-medium text-2xl">Cart</h1>
      <div className="text-black flex gap-2">
        <p className="font-medium">Total:</p>
        <p className="">${Math.round(cart_items.total * 100) / 100}</p>
      </div>
    </div>
    <ul className="flex gap-1 flex-col w-full place-items-center">
      {cart_items.items.map((e, idx) => (
        <li
          className="bg-gray-800 rounded sm:w-130 w-80 p-1 truncate hover:scale-101 hover:bg-gray-600 flex justify-between transition-all"
          key={idx}
          title={`${e.name}`}>
            <div className="flex justify-between w-full pr-2">
            <p className="truncate sm:w-full w-30">{e.name}</p>
            <p className="text-green-600">${e.value}</p>
            </div>
            <button className="bg-red-600 rounded px-1 text-white cursor-pointer transition-all hove:scale-101 hover:bg-red-500" onClick={() => delete_item({item: e})}>
              <CruiseIcon />
            </button>
        </li>
      ))}
    </ul>
  </main>
}

export default Cart