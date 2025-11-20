import { useNavigate } from "react-router-dom";
import { useItemStore } from "@/store/item_store";
import { useLoadItemEffect } from "@/hooks/useloaditem";

const Products = () => {
  const navigate = useNavigate();
  const { add_all_items, add_error, items, is_loading, set_is_loading } =
    useItemStore((state) => state);
  useLoadItemEffect({
    setItemStore: add_all_items,
    setError: add_error,
    items,
    is_loading,
    set_is_loading,
  });

  const redirect_to_details = ({ id }: { id: number }) => {
    return navigate(`/itemdetails/${id}`);
  };

  return (
    <section className="grid grid-cols-3 md:grid-cols-5 gap-4">
      {items.map((item, index) => {
        return (
          <div
            key={index}
            className="h-60 w-30 bg-white rounded text-gray-800 cursor-pointer hover:scale-[102%] transition-all"
            onClick={() => redirect_to_details({ id: item.id! })}
          >
            <img
              src={`https://picsum.photos/200/320`}
              className="rounded-t-sm w-[120px] h-[190px]"
              alt={item.name}
            />
            <h2 className="mx-1 truncate" title={item.name}>
              {item.name}
            </h2>
            <p className="text-green-600 mx-1">${item.value}</p>
          </div>
        );
      })}
    </section>
  );
};

export default Products;
