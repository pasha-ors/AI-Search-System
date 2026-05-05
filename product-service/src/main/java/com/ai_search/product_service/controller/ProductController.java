package com.ai_search.product_service.controller;

import com.ai_search.product_service.dto.SearchRequest;
import com.ai_search.product_service.entity.Product;
import com.ai_search.product_service.service.ProductService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService service;

    @PostMapping("/search")
    public List<Product> search(@RequestBody SearchRequest request) {
        return service.search(request);
    }

}
