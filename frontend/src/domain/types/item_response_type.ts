import { type Item } from "./item_type";

export type ItemResponse = {
  page: number;
  data: Item[]
}