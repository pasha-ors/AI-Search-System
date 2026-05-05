package com.ai_search.search_service.client;

import com.ai_search.search_service.dto.LlmResponse;
import com.ai_search.search_service.dto.SearchRequest;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Component
public class LlmClient {

    @Value("${llm.service.url}")
    private String url;

    private final RestTemplate rest = new RestTemplate();

    public SearchRequest extract(String text) {

        Map<String, String> body = Map.of("text", text);

        LlmResponse response = rest.postForObject(
                url + "/analyze",
                body,
                LlmResponse.class
        );

        return response != null ? response.data() : null;
    }
}
