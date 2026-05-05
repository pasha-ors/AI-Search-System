package com.ai_search.product_service.repository;

import com.ai_search.product_service.entity.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {

    @Query("""
SELECT p FROM Product p
WHERE
    (:color IS NULL OR p.color IN :color)
AND (:brand IS NULL OR p.brand IN :brand)
AND (:purpose IS NULL OR p.purpose IN :purpose)
AND (:maxPrice IS NULL OR p.price <= :maxPrice)
AND (:minPrice IS NULL OR p.price >= :minPrice)
""")
    List<Product> search(
            @Param("color") List<String> color,
            @Param("brand") List<String> brand,
            @Param("purpose") List<String> purpose,
            @Param("maxPrice") Integer maxPrice,
            @Param("minPrice") Integer minPrice
    );

}
