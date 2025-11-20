import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useLoadItemEffect } from './useloaditem';
import { type Item } from '@/domain/types/item_type';

// Mock global fetch
global.fetch = vi.fn();

describe('useLoadItemEffect Hook', () => {
  const mockSetItemStore = vi.fn();
  const mockSetError = vi.fn();
  const mockSetIsLoading = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('should fetch items when items array is empty and not loading', async () => {
    const mockItems: Item[] = [
      {
        id: 1,
        name: 'Test Product',
        value: 100,
        image_url: 'https://example.com/image.jpg',
      },
    ];

    const mockResponse = {
      data: mockItems,
    };

    vi.mocked(global.fetch).mockResolvedValueOnce({
      json: async () => mockResponse,
      ok: true,
    } as Response);

    renderHook(() =>
      useLoadItemEffect({
        setItemStore: mockSetItemStore,
        setError: mockSetError,
        items: [],
        is_loading: false,
        set_is_loading: mockSetIsLoading,
      })
    );

    await waitFor(() => {
      expect(mockSetIsLoading).toHaveBeenCalled();
    });

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/item/');
    });

    await waitFor(() => {
      expect(mockSetItemStore).toHaveBeenCalledWith(mockItems);
    });
  });

  it('should not fetch if items already exist', () => {
    const existingItems: Item[] = [
      {
        id: 1,
        name: 'Existing Product',
        value: 50,
        image_url: 'https://example.com/existing.jpg',
      },
    ];

    renderHook(() =>
      useLoadItemEffect({
        setItemStore: mockSetItemStore,
        setError: mockSetError,
        items: existingItems,
        is_loading: false,
        set_is_loading: mockSetIsLoading,
      })
    );

    expect(global.fetch).not.toHaveBeenCalled();
    expect(mockSetIsLoading).not.toHaveBeenCalled();
  });

  it('should not fetch if already loading', () => {
    renderHook(() =>
      useLoadItemEffect({
        setItemStore: mockSetItemStore,
        setError: mockSetError,
        items: [],
        is_loading: true,
        set_is_loading: mockSetIsLoading,
      })
    );

    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('should handle fetch errors', async () => {
    const mockError = new Error('Network error');

    vi.mocked(global.fetch).mockRejectedValueOnce(mockError);

    renderHook(() =>
      useLoadItemEffect({
        setItemStore: mockSetItemStore,
        setError: mockSetError,
        items: [],
        is_loading: false,
        set_is_loading: mockSetIsLoading,
      })
    );

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/item/');
    });

    await waitFor(() => {
      expect(mockSetError).toHaveBeenCalledWith(mockError);
    });

    await waitFor(() => {
      expect(mockSetItemStore).not.toHaveBeenCalled();
    });
  });

  it('should call set_is_loading in finally block', async () => {
    const mockItems: Item[] = [
      {
        id: 1,
        name: 'Test Product',
        value: 100,
        image_url: 'https://example.com/image.jpg',
      },
    ];

    vi.mocked(global.fetch).mockResolvedValueOnce({
      json: async () => ({ data: mockItems }),
      ok: true,
    } as Response);

    renderHook(() =>
      useLoadItemEffect({
        setItemStore: mockSetItemStore,
        setError: mockSetError,
        items: [],
        is_loading: false,
        set_is_loading: mockSetIsLoading,
      })
    );

    await waitFor(() => {
      // Should be called twice: once before fetch and once in finally
      expect(mockSetIsLoading).toHaveBeenCalledTimes(2);
    });
  });

  it('should fetch with correct backend URL', async () => {
    vi.mocked(global.fetch).mockResolvedValueOnce({
      json: async () => ({ data: [] }),
      ok: true,
    } as Response);

    renderHook(() =>
      useLoadItemEffect({
        setItemStore: mockSetItemStore,
        setError: mockSetError,
        items: [],
        is_loading: false,
        set_is_loading: mockSetIsLoading,
      })
    );

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/item/');
    });
  });
});
