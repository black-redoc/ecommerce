import { type Item } from "@/domain/types/item_type";
import { useParams, Navigate } from "react-router-dom";
import { useItemStore } from "@/store/item_store";
import StarEmptyIcon from "@/components/icons/star-empty";
import StarFillIcon from "@/components/icons/star-fill";
import CartIcon from "@/components/icons/cart";
import Navbar from "@/components/navbar";
import { useLoadItemEffect } from "@/hooks/useloaditem";
import { useCartStore } from "@/store/cart_store";

const ItemDetail = () => {
  const { id } = useParams();
  const { add_item } = useCartStore((state) => state)
  const { items, add_all_items, add_error, is_loading, set_is_loading } =
    useItemStore((state) => state);
  useLoadItemEffect({
    setItemStore: add_all_items,
    setError: add_error,
    items,
    is_loading,
    set_is_loading,
  });
  if (is_loading) {
    return (
      <main className="h-screen flex place-items-center place-content-center w-screen">
        <h1 className="text-3xl font-bold">loading</h1>
      </main>
    );
  }
  const item = items.find((e: Item) => e.id == id);
  const add_to_cart = ({item}: {item: Item}) => {
    add_item(item)
  }

  if (!item) {
    return <Navigate to="/not-found" replace />;
  }
  return (
    <main className="mt-10 flex place-items-center place-content-center w-screen">
      <Navbar />
      <section className="sm:px-0 px-1 mt-3 sm:mt-0">
        <div className="flex justify-between">
          <h1 className="text-bold text-2xl text-black">{item.name}</h1>
          <div className="flex gap-1">
            <StarFillIcon />
            <StarFillIcon />
            <StarFillIcon />
            <StarEmptyIcon />
            <StarEmptyIcon />
          </div>
        </div>
        <img
          className="rounded w-[400px] h-[500px]"
          src={`https://picsum.photos/500/500`}
          alt={item.name}
        />
        <div className="flex justify-between w-full mt-3 px-1">
          <p className="text-green-400 font-medium text-2xl truncate py-2">
            ${item.value}
          </p>
          <button className="flex place-items-center gap-2 text-white bg-blue-600 px-2 rounded cursor-pointer transition-all hover:scale-101 hover:bg-blue-500" onClick={() => add_to_cart({item})}>
            <p>Agregar al carrito</p>
            <CartIcon />
          </button>
        </div>
        <h3 className="text-black font-medium mt-3">Description:</h3>
        <p className="w-100 text-black">
          Lorem ipsum dolor, sit amet consectetur adipisicing elit. Ipsum
          quaerat natus veniam magni, voluptatum optio similique odio cumque
          totam omnis eius soluta nesciunt minima aliquid. Provident earum
          similique accusantium nisi?
        </p>
      </section>
    </main>
  );
};

export default ItemDetail;
