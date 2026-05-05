package com.internship.tool.service;

import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.RestClientException;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import java.time.Duration;
import java.util.Map;
import java.util.HashMap;

public class AiServiceClient {
    private final RestTemplate restTemplate;
    private final String baseUrl = "http://localhost:5000";

    public AiServiceClient() {
        restTemplate = new RestTemplate();
        HttpComponentsClientHttpRequestFactory factory = new HttpComponentsClientHttpRequestFactory();
        factory.setConnectTimeout(Duration.ofSeconds(10));
        factory.setReadTimeout(Duration.ofSeconds(10));
        restTemplate.setRequestFactory(factory);
    }

    public Map<String, Object> describe(String vendorName, String riskFactors) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            Map<String, String> body = new HashMap<>();
            body.put("vendor_name", vendorName);
            body.put("risk_factors", riskFactors);
            HttpEntity<Map<String, String>> entity = new HttpEntity<>(body, headers);
            return restTemplate.postForObject(baseUrl + "/describe", entity, Map.class);
        } catch (RestClientException e) {
            return null;
        }
    }

    public Map<String, Object> recommend(String vendorName, String riskFactors) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            Map<String, String> body = new HashMap<>();
            body.put("vendor_name", vendorName);
            body.put("risk_factors", riskFactors);
            HttpEntity<Map<String, String>> entity = new HttpEntity<>(body, headers);
            return restTemplate.postForObject(baseUrl + "/recommend", entity, Map.class);
        } catch (RestClientException e) {
            return null;
        }
    }

    public Map<String, Object> generateReport(String vendorName, String riskFactors) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            Map<String, String> body = new HashMap<>();
            body.put("vendor_name", vendorName);
            body.put("risk_factors", riskFactors);
            HttpEntity<Map<String, String>> entity = new HttpEntity<>(body, headers);
            return restTemplate.postForObject(baseUrl + "/generate-report", entity, Map.class);
        } catch (RestClientException e) {
            return null;
        }
    }
}