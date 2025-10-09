'use client'

import React, { useEffect, useState } from 'react';
import axios, { AxiosError } from 'axios';
import Movie from '@/app/interfaces/Movie'

const MoviesTable = () => {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<AxiosError>();
  const [sort, setSort] = useState('id');
  const [order, setOrder] = useState<'asc' | 'desc'>('asc');
  const [genre, setGenre] = useState('');
  const [genreInput, setGenreInput] = useState('');
  const [page, setPage] = useState(1);
  const [size] = useState(10);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';


  useEffect(() => {
    const handler = setTimeout(() => {
      setGenre(genreInput);
      setPage(1);
    }, 500);
    return () => clearTimeout(handler);
  }, [genreInput]);

  useEffect(() => {
    const fetchMovies = async () => {
      setLoading(true);
      try {
        const params = {
          ...(genre && { genre }),
          ...(sort && { sort }),
          ...(order && { order }),
          ...(page && { page }),
          ...(size && { size }),
        };

        const response = await axios.get(apiUrl + '/movies', { params });
        setMovies(response.data);
      } catch (err) {
        setError(err as AxiosError);
      } finally {
        setLoading(false);
      }
    };

    fetchMovies();
  }, [genre, sort, order, page]);

  const handleSortChange = (newSort: string) => {
    if (sort === newSort) {
      setOrder(order === 'asc' ? 'desc' : 'asc');
    } else {
      setPage(1);
      setSort(newSort);
      setOrder('asc');
    }
  };

  if (loading) return <div className="text-center py-8 text-gray-600">Loading...</div>;
  if (error) return <div className="text-center text-red-500">Error: {error.message}</div>;

  return (
    <div className="max-w-5xl mx-auto p-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-semibold text-gray-800">Movies</h1>
        <input
          type="text"
          placeholder="Filter by genre..."
          value={genreInput}
          onChange={(e) => setGenreInput(e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div className="bg-white shadow-md rounded-lg overflow-auto text-xs sm:text-sm">
        <table className="border-collapse min-w-full table-fixed">
          <thead>
            <tr className="bg-gray-100 text-left text-gray-700 uppercase text-sm">
              {['id', 'title', 'genre', 'released'].map((header) => (
                <th
                  key={header}
                  onClick={() => handleSortChange(header)}
                  className="cursor-pointer py-3 px-4 font-medium hover:text-blue-600"
                >
                  {header}
                  {sort === header && (
                    <span className="ml-1 text-xs">{order === 'asc' ? '▲' : '▼'}</span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {movies.length > 0 ? (
              movies.map((movie) => (
                <tr key={movie.id} className="border-b hover:bg-gray-50">
                  <td align={'center'} className="py-3 px-4 text-gray-700">{movie.id}</td>
                  <td className="py-3 px-4 text-gray-800 font-medium">{movie.title}</td>
                  <td className="py-3 px-4 text-gray-600">{movie.genre}</td>
                  <td className="py-3 px-4 text-gray-600">{movie.released}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={4} className="text-center py-6 text-gray-500">
                  No movies found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="flex justify-between items-center mt-4">
        <button
          onClick={() => setPage(page - 1)}
          disabled={page === 1}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg disabled:opacity-50 hover:bg-gray-300"
        >
          Previous
        </button>
        <span className="text-gray-600 text-sm">Page {page}</span>
        <button
          onClick={() => {
            if (movies.length > 0) {
              setPage(page + 1)
            }
          }}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default MoviesTable;
