import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'

function Items() {
  const [items, setItems] = useState([])
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [editingItem, setEditingItem] = useState(null)
  const [error, setError] = useState('')
  const limit = 10
  const navigate = useNavigate()

  const totalPages = Math.ceil(total / limit)

  const fetchItems = async () => {
    try {
      const res = await api.get('/items', { params: { page, limit } })
      setItems(res.data.data)
      setTotal(res.data.total)
    } catch (err) {
      setError('Failed to fetch items')
    }
  }

  useEffect(() => {
    fetchItems()
  }, [page])

  const handleCreate = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await api.post('/items', { title, description })
      setTitle('')
      setDescription('')
      fetchItems()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create item')
    }
  }

  const handleToggleComplete = async (item) => {
    try {
      await api.put(`/items/${item.item_id}`, { completed: !item.completed })
      fetchItems()
    } catch (err) {
      setError('Failed to update item')
    }
  }

  const handleUpdate = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await api.put(`/items/${editingItem.item_id}`, {
        title: editingItem.title,
        description: editingItem.description,
      })
      setEditingItem(null)
      fetchItems()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update item')
    }
  }

  const handleDelete = async (item_id) => {
    try {
      await api.delete(`/items/${item_id}`)
      fetchItems()
    } catch (err) {
      setError('Failed to delete item')
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <div>
      <div>
        <h2>My Items</h2>
        <button onClick={handleLogout}>Logout</button>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {/* Create form */}
      <form onSubmit={handleCreate}>
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button type="submit">Add Item</button>
      </form>

      {/* Items list */}
      <ul>
        {items.map((item) => (
          <li key={item.item_id}>
            {editingItem?.item_id === item.item_id ? (
              <form onSubmit={handleUpdate}>
                <input
                  type="text"
                  value={editingItem.title}
                  onChange={(e) => setEditingItem({ ...editingItem, title: e.target.value })}
                  required
                />
                <input
                  type="text"
                  value={editingItem.description || ''}
                  onChange={(e) => setEditingItem({ ...editingItem, description: e.target.value })}
                />
                <button type="submit">Save</button>
                <button type="button" onClick={() => setEditingItem(null)}>Cancel</button>
              </form>
            ) : (
              <div>
                <input
                  type="checkbox"
                  checked={item.completed}
                  onChange={() => handleToggleComplete(item)}
                />
                <span style={{ textDecoration: item.completed ? 'line-through' : 'none' }}>
                  {item.title}
                </span>
                {item.description && <span> — {item.description}</span>}
                <button onClick={() => setEditingItem(item)}>Edit</button>
                <button onClick={() => handleDelete(item.item_id)}>Delete</button>
              </div>
            )}
          </li>
        ))}
      </ul>

      {/* Pagination */}
      {totalPages > 1 && (
        <div>
          <button onClick={() => setPage((p) => p - 1)} disabled={page === 1}>Prev</button>
          <span> Page {page} of {totalPages} </span>
          <button onClick={() => setPage((p) => p + 1)} disabled={page === totalPages}>Next</button>
        </div>
      )}
    </div>
  )
}

export default Items