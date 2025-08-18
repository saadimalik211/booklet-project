# MVP Roadmap & Goals

## MVP Goal
**Create a working PDF booklet generator that can merge static PDFs and render Excel tabs as PDF pages, with a simple web interface for uploading files and triggering generation.**

## MVP Roadmap (8-12 weeks)

### Phase 1: Core Infrastructure (Weeks 1-3)
**Goal: Basic API + PDF merging + simple UI**

#### Week 1: Setup & Basic API
- Initialize FastAPI project with SQLAlchemy + PostgreSQL
- Create basic models: `Customer`, `Book`, `Page`
- Implement CRUD endpoints for books and pages
- Add file upload handling for PDFs

#### Week 2: PDF Processing Core
- Implement `PyPDF2` merging functionality
- Add static page support (upload PDF → merge into book)
- Create basic PDF generation endpoint
- Add simple form filling with `ReportLab`

#### Week 3: Basic UI
- Simple React frontend with Tailwind
- Book creation/editing interface
- File upload for PDFs
- Trigger PDF generation

### Phase 2: Excel Integration (Weeks 4-6)
**Goal: Excel tab rendering + customer attributes**

#### Week 4: Excel Processing
- Implement `openpyxl` + `ReportLab` Excel tab → PDF
- Add Excel page type to book definitions
- Handle spreadsheet uploads
- Basic tab selection UI

#### Week 5: Customer System
- Customer CRUD with attributes (key-value pairs)
- Year/quarter versioning for attributes
- Customer selection in UI
- Basic attribute editing

#### Week 6: Choosable Pages
- Implement conditional page logic based on customer attributes
- Add choosable page type
- UI for defining attribute-based page selection rules

### Phase 3: Production Features (Weeks 7-9)
**Goal: Background processing + polish**

#### Week 7: Async Processing
- Add Celery + Redis for background PDF generation
- Job status tracking
- Progress indicators in UI
- Download links for completed PDFs

#### Week 8: Error Handling & Validation
- Comprehensive error handling
- Input validation (file types, sizes, required fields)
- Logging and monitoring
- User feedback for failed generations

#### Week 9: Polish & Testing
- UI/UX improvements
- End-to-end testing
- Performance optimization
- Documentation

### Phase 4: Advanced Features (Weeks 10-12)
**Goal: Enhanced functionality**

#### Week 10: Advanced PDF Features
- Better form filling with `borb` or `pdfrw`
- PDF metadata and bookmarks
- Page numbering and headers/footers

#### Week 11: Enhanced Excel Rendering
- Better table formatting with `ReportLab`
- Support for charts and images
- Multiple tab handling in single page

#### Week 12: Production Deployment
- Docker containerization
- Environment configuration
- Basic monitoring and logging
- Deployment documentation

---

## MVP Success Criteria

### Must Have (Phase 1-2)
- ✅ Upload and merge static PDFs
- ✅ Render Excel tabs as PDF pages
- ✅ Basic customer attribute system
- ✅ Simple web interface
- ✅ Generate downloadable PDF booklets

### Should Have (Phase 3)
- ✅ Background processing (Celery)
- ✅ Error handling and validation
- ✅ Job status tracking
- ✅ Basic logging

### Nice to Have (Phase 4)
- ✅ Advanced PDF form filling
- ✅ Better Excel formatting
- ✅ Production deployment
- ✅ Monitoring and analytics

---

## Technical Decisions for MVP

### Keep Simple
- **Database**: PostgreSQL + SQLAlchemy (no complex migrations initially)
- **File Storage**: Local filesystem (move to S3 later)
- **Authentication**: Basic session-based (add JWT later)
- **UI**: Simple forms, no complex drag-and-drop initially

### Focus Areas
1. **PDF Processing**: Get basic merging working reliably
2. **Excel Integration**: Simple tab → PDF conversion
3. **User Experience**: Clear workflow from upload → generation → download
4. **Error Handling**: Graceful failures with helpful messages

### Defer for Later
- Complex PDF form manipulation
- Advanced Excel formatting
- Multi-user authentication
- Cloud deployment
- Advanced monitoring

---

## Risk Mitigation

### Technical Risks
- **PDF Library Complexity**: Start with `PyPDF2` + `ReportLab`, add advanced libraries later
- **Excel Rendering**: Use simple text-based rendering initially, enhance formatting later
- **Performance**: Use background processing from the start

### Timeline Risks
- **Scope Creep**: Stick to core PDF merging + Excel rendering
- **Integration Complexity**: Build and test each component independently
- **UI Complexity**: Start with simple forms, enhance UX iteratively

---

## Development Guidelines

### Code Organization
- Follow the structure established in `mockup/`
- Separate concerns: API, worker, document processing
- Use type hints and docstrings
- Implement comprehensive error handling

### Testing Strategy
- Unit tests for PDF/Excel processing functions
- Integration tests for API endpoints
- End-to-end tests for complete workflows
- Manual testing for UI interactions

### Documentation
- API documentation with FastAPI auto-generation
- Code comments for complex business logic
- User guides for common workflows
- Deployment and setup instructions

---

## Success Metrics

### Technical Metrics
- PDF generation success rate > 95%
- Average generation time < 30 seconds
- Zero data loss during processing
- < 5% error rate on user operations

### User Experience Metrics
- Time to first successful PDF generation < 5 minutes
- User satisfaction with output quality
- Reduction in manual PDF creation time
- Adoption rate of new features

### Business Metrics
- Number of PDFs generated per week
- Customer retention and satisfaction
- Time saved per customer
- Cost reduction in manual processes
