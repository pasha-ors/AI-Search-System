package com.ai_search.search_service.controller;

import com.ai_search.search_service.client.ProductDto;
import com.ai_search.search_service.dto.QueryRequest;
import com.ai_search.search_service.service.SearchService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/search")
@RequiredArgsConstructor
public class SearchController {

    private final SearchService searchService;

    @PostMapping
    public List<ProductDto> search(@RequestBody QueryRequest request)
    {
        return searchService.search(request.text());
    }
}
