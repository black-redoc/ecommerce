import { useEffect } from "react";
import { type ItemResponse } from "@/domain/types/item_response_type";
import { type Item } from "@/domain/types/item_type";
type LoadItemType = {
  setItemStore: (_: Item[]) => Promise<any>;
  setError: (_: any) => Promise<void>;
  items: Item[];
  is_loading: boolean;
  set_is_loading: () => void;
};

const backend_url = "http://localhost:8000/item/";

export const useLoadItemEffect = ({
  setItemStore,
  setError,
  items,
  is_loading,
  set_is_loading,
}: LoadItemType) => {
  return useEffect(() => {
    if (items.length || is_loading) {
      return;
    }
    set_is_loading();
    fetch(backend_url)
      .then((response) => response.json())
      .then((value: ItemResponse) => {
        setItemStore(value.data);
      })
      .catch((error: any) => {
        setError(error);
      }).finally(() => {
        set_is_loading()
      });
  }, []);
};
