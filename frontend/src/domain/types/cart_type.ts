import { type Item } from "@/domain/types/item_type";

export type Cart = {
  id: number | undefined;
  items: Item[];
  total: number;
  count: number;
};
