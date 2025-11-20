import { create } from "zustand";
import { type Item } from "@/domain/types/item_type";

export type ItemStore = {
  items: Item[];
  error: any;
  add_all_items: (item: Item[]) => Promise<void>;
  add_error: (error: any) => Promise<void>;
  is_loading: boolean;
  set_is_loading: () => void;
};

export const useItemStore = create<ItemStore>((set) => ({
  items: [] as Item[],
  set_is_loading: () =>
    set((state) => ({ ...state, is_loading: !state.is_loading })),
  is_loading: false,
  error: undefined,
  add_all_items: async (items: Item[]) => {
    set(() => ({
      items: items,
    }));
  },
  add_error: async (error: any) => {
    set((state) => ({
      ...state,
      error,
    }));
  },
}));
