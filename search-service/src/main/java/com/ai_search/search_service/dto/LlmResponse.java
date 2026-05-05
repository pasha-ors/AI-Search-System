package com.ai_search.search_service.dto;

public record LlmResponse(
        boolean success,
        SearchRequest data
) {}
