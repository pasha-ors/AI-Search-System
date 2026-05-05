package com.ai_search.product_service.service;

import com.ai_search.product_service.dto.SearchRequest;
import com.ai_search.product_service.entity.Product;
import com.ai_search.product_service.repository.ProductRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository repository;

    public List<Product> search(SearchRequest req) {
        return repository.search(
                normalize(req.color()),
                normalize(req.brand()),
                normalize(req.purpose()),
                req.max_price(),
                req.min_price()
        );
    }

    private List<String> normalize(List<String> list) {
        return (list == null || list.isEmpty()) ? null : list;
    }



}
