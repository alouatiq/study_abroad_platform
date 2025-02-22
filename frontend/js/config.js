const config = {
    API_URL: 'http://localhost:8000',
    DEFAULT_CURRENCY: '€',
    DATE_FORMAT: 'YYYY-MM-DD',
    UPLOAD_MAX_SIZE: 5 * 1024 * 1024, // 5MB
    SUPPORTED_DOCUMENT_TYPES: ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png'],
    REFRESH_INTERVAL: 30000, // 30 seconds - for polling updates
};

// Prevent accidental modifications
Object.freeze(config);
