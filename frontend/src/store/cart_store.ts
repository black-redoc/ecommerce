import { create } from "zustand";
import { type Item } from "@/domain/types/item_type";
import { type Cart } from "@/domain/types/cart_type";

type CartStore = {
  data: Cart;
  add_item: (item: Item) => Promise<void>;
  delete_item: (item: Item) => Promise<void>;
};

export const useCartStore = create<CartStore>((set) => ({
  data: {
    id: 0,
    items: [] as Item[],
    total: 0,
    count: 0,
  },
  add_item: async (item: Item) => {
    set((state) => {
      if (state.data.items.map((e) => e.id).includes(item.id)) {
        return state;
      }
      return {
        ...state,
        data: {
          id: state.data.id,
          items: [...state.data.items, item],
          total: state.data.total + item.value,
          count: state.data.count + 1,
        },
      };
    });
  },
  delete_item: async (item: Item) => {
    set((state) => {
      if (!state.data.items.map((e) => e.id).includes(item.id)) {
        return state;
      }
      return {
        ...state,
        data: {
          id: state.data.id,
          items: state.data.items.filter((e) => e.id !== item.id),
          total: state.data.total - item.value,
          count: state.data.count - 1,
        },
      };
    });
  },
}));
