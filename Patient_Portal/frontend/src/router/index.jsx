import { createBrowserRouter } from 'react-router-dom'
import LoginPage from '../Components/LoginPage/LoginPage'
import Schedule from '../Components/Schedule/Schedule'

export const router = createBrowserRouter([
    {
        path: '/',
        element: <LoginPage />,
    },
    {
        path: '/schedule',
        element: <Schedule />,
    },
]);