package com.ai_search.search_service.client;

import com.ai_search.search_service.dto.SearchRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@Component
public class ProductClient {

    @Value("${product.url}")
    private String url;

    private final RestTemplate rest = new RestTemplate();

    public List<ProductDto> search(SearchRequest request) {

        ResponseEntity<List<ProductDto>> response = rest.exchange(
                url + "/products/search",
                HttpMethod.POST,
                new HttpEntity<>(request),
                new ParameterizedTypeReference<List<ProductDto>>() {}
        );

        return response.getBody();
    }

}
