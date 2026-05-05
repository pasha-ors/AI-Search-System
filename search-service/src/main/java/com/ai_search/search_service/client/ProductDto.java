package com.ai_search.search_service.client;

public record ProductDto(
        Long id,

        String name,

        String brand,

        String color,

        String purpose,

        Integer price
){}
