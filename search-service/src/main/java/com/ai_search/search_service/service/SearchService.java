package com.ai_search.search_service.service;

import com.ai_search.search_service.client.LlmClient;
import com.ai_search.search_service.client.ProductClient;
import com.ai_search.search_service.client.ProductDto;
import com.ai_search.search_service.dto.SearchRequest;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;


@Slf4j
@Service
@RequiredArgsConstructor
public class SearchService {

    private final LlmClient llm;
    private final ProductClient productClient;

    public List<ProductDto> search(String text){
        SearchRequest filter = llm.extract(text);

        return productClient.search(filter);
    }
}
