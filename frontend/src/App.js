import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CocktailTable from './CocktailTable';
import ProductDetailPage from './ProductDetailPage';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<CocktailTable />} />
                <Route path="/products/:productId" element={<ProductDetailPage />} />
            </Routes>
        </Router>
    );
};

export default App;
