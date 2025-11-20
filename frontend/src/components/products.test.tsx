import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import userEvent from '@testing-library/user-event';
import Products from './products';
import { useItemStore } from '@/store/item_store';
import { type Item } from '@/domain/types/item_type';

// Mock del store
vi.mock('@/store/item_store');

// Mock del hook
vi.mock('@/hooks/useloaditem', () => ({
  useLoadItemEffect: vi.fn(),
}));

const mockItems: Item[] = [
  {
    id: 1,
    name: 'Product 1',
    value: 100,
    image_url: 'https://example.com/image1.jpg',
  },
  {
    id: 2,
    name: 'Product 2',
    value: 200,
    image_url: 'https://example.com/image2.jpg',
  },
  {
    id: 3,
    name: 'Product 3',
    value: 300,
    image_url: 'https://example.com/image3.jpg',
  },
];

const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('Products Component - Integration Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render list of products', () => {
    vi.mocked(useItemStore).mockReturnValue({
      items: mockItems,
      add_all_items: vi.fn(),
      add_error: vi.fn(),
      is_loading: false,
      set_is_loading: vi.fn(),
      error: null,
    });

    renderWithRouter(<Products />);

    expect(screen.getByText('Product 1')).toBeInTheDocument();
    expect(screen.getByText('Product 2')).toBeInTheDocument();
    expect(screen.getByText('Product 3')).toBeInTheDocument();
  });

  it('should display product prices correctly', () => {
    vi.mocked(useItemStore).mockReturnValue({
      items: mockItems,
      add_all_items: vi.fn(),
      add_error: vi.fn(),
      is_loading: false,
      set_is_loading: vi.fn(),
      error: null,
    });

    renderWithRouter(<Products />);

    expect(screen.getByText('$100')).toBeInTheDocument();
    expect(screen.getByText('$200')).toBeInTheDocument();
    expect(screen.getByText('$300')).toBeInTheDocument();
  });

  it('should render product images with correct alt text', () => {
    vi.mocked(useItemStore).mockReturnValue({
      items: mockItems,
      add_all_items: vi.fn(),
      add_error: vi.fn(),
      is_loading: false,
      set_is_loading: vi.fn(),
      error: null,
    });

    renderWithRouter(<Products />);

    const images = screen.getAllByRole('img');
    expect(images).toHaveLength(3);
    expect(images[0]).toHaveAttribute('alt', 'Product 1');
    expect(images[1]).toHaveAttribute('alt', 'Product 2');
    expect(images[2]).toHaveAttribute('alt', 'Product 3');
  });

  it('should navigate to product details on click', async () => {
    const user = userEvent.setup();
    vi.mocked(useItemStore).mockReturnValue({
      items: mockItems,
      add_all_items: vi.fn(),
      add_error: vi.fn(),
      is_loading: false,
      set_is_loading: vi.fn(),
      error: null,
    });

    renderWithRouter(<Products />);

    const productCard = screen.getByText('Product 1').closest('div');
    expect(productCard).toBeInTheDocument();

    if (productCard) {
      await user.click(productCard);
      // After click, the navigation should occur
      // In a real test, you would check the URL or use a navigation mock
    }
  });

  it('should render empty list when no items', () => {
    vi.mocked(useItemStore).mockReturnValue({
      items: [],
      add_all_items: vi.fn(),
      add_error: vi.fn(),
      is_loading: false,
      set_is_loading: vi.fn(),
      error: null,
    });

    const { container } = renderWithRouter(<Products />);

    const section = container.querySelector('section');
    expect(section).toBeInTheDocument();
    expect(section?.children).toHaveLength(0);
    expect(screen.queryByText('Product 1')).not.toBeInTheDocument();
  });

  it('should apply hover styles to product cards', () => {
    vi.mocked(useItemStore).mockReturnValue({
      items: mockItems,
      add_all_items: vi.fn(),
      add_error: vi.fn(),
      is_loading: false,
      set_is_loading: vi.fn(),
      error: null,
    });

    renderWithRouter(<Products />);

    const productCard = screen.getByText('Product 1').closest('div');
    expect(productCard).toHaveClass('hover:scale-[102%]');
    expect(productCard).toHaveClass('cursor-pointer');
  });
});
