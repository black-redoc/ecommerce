import { describe, it, expect, beforeEach } from 'vitest';
import { useCartStore } from './cart_store';
import { type Item } from '@/domain/types/item_type';

describe('Cart Store', () => {
  beforeEach(() => {
    // Reset store state before each test
    useCartStore.setState({
      data: {
        id: 0,
        items: [],
        total: 0,
        count: 0,
      },
    });
  });

  describe('add_item', () => {
    it('should add an item to the cart', async () => {
      const testItem: Item = {
        id: 1,
        name: 'Test Product',
        value: 100,
        image_url: 'https://example.com/image.jpg',
      };

      await useCartStore.getState().add_item(testItem);

      const state = useCartStore.getState();
      expect(state.data.items).toHaveLength(1);
      expect(state.data.items[0]).toEqual(testItem);
      expect(state.data.count).toBe(1);
      expect(state.data.total).toBe(100);
    });

    it('should not add duplicate items', async () => {
      const testItem: Item = {
        id: 1,
        name: 'Test Product',
        value: 100,
        image_url: 'https://example.com/image.jpg',
      };

      await useCartStore.getState().add_item(testItem);
      await useCartStore.getState().add_item(testItem); // Try to add again

      const state = useCartStore.getState();
      expect(state.data.items).toHaveLength(1);
      expect(state.data.count).toBe(1);
      expect(state.data.total).toBe(100);
    });

    it('should add multiple different items', async () => {
      const item1: Item = {
        id: 1,
        name: 'Product 1',
        value: 100,
        image_url: 'https://example.com/image1.jpg',
      };

      const item2: Item = {
        id: 2,
        name: 'Product 2',
        value: 200,
        image_url: 'https://example.com/image2.jpg',
      };

      await useCartStore.getState().add_item(item1);
      await useCartStore.getState().add_item(item2);

      const state = useCartStore.getState();
      expect(state.data.items).toHaveLength(2);
      expect(state.data.count).toBe(2);
      expect(state.data.total).toBe(300);
    });
  });

  describe('delete_item', () => {
    it('should remove an item from the cart', async () => {
      const testItem: Item = {
        id: 1,
        name: 'Test Product',
        value: 100,
        image_url: 'https://example.com/image.jpg',
      };

      await useCartStore.getState().add_item(testItem);
      await useCartStore.getState().delete_item(testItem);

      const state = useCartStore.getState();
      expect(state.data.items).toHaveLength(0);
      expect(state.data.count).toBe(0);
      expect(state.data.total).toBe(0);
    });

    it('should not affect cart if item does not exist', async () => {
      const item1: Item = {
        id: 1,
        name: 'Product 1',
        value: 100,
        image_url: 'https://example.com/image1.jpg',
      };

      const item2: Item = {
        id: 2,
        name: 'Product 2',
        value: 200,
        image_url: 'https://example.com/image2.jpg',
      };

      await useCartStore.getState().add_item(item1);
      await useCartStore.getState().delete_item(item2); // Try to delete non-existent item

      const state = useCartStore.getState();
      expect(state.data.items).toHaveLength(1);
      expect(state.data.count).toBe(1);
      expect(state.data.total).toBe(100);
    });

    it('should correctly update total when removing an item', async () => {
      const item1: Item = {
        id: 1,
        name: 'Product 1',
        value: 100,
        image_url: 'https://example.com/image1.jpg',
      };

      const item2: Item = {
        id: 2,
        name: 'Product 2',
        value: 200,
        image_url: 'https://example.com/image2.jpg',
      };

      await useCartStore.getState().add_item(item1);
      await useCartStore.getState().add_item(item2);
      await useCartStore.getState().delete_item(item1);

      const state = useCartStore.getState();
      expect(state.data.items).toHaveLength(1);
      expect(state.data.items[0]).toEqual(item2);
      expect(state.data.count).toBe(1);
      expect(state.data.total).toBe(200);
    });
  });
});
