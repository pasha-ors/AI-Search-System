package com.ai_search.search_service.dto;

import java.util.List;

public record SearchRequest(
        List<String> color,
        List<String> brand,
        List<String> purpose,
        Integer max_price,
        Integer min_price
) {}
