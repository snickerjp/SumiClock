# Kiroween Hackathon Submission Guidelines

## Hackathon Overview

### Key Information
- **Event**: Kiroween 2025
- **Deadline**: December 5, 2025 @ 2:00 PM Pacific Time (December 6, 2025 @ 7:00 AM JST)
- **Sponsor**: Amazon Web Services (AWS)
- **Platform**: Devpost

### SumiClock Category
**Primary Category**: Resurrection
- Bringing E-paper display technology (Kindle, Kobo) back to life
- Reimagining "obsolete" E-ink technology with modern web APIs
- Solving the problem of displaying real-time information on low-power devices

**Alternative Category**: Costume Contest
- Minimalist, polished UI design
- Haunting simplicity and elegance
- E-paper aesthetic (black & white, high contrast)

## Submission Requirements

### Must-Have Elements

#### 1. Code Repository
- ✅ Public GitHub repository
- ✅ OSI-approved open source license (MIT)
- ✅ All source code, assets, and instructions included
- ✅ License visible in repository About section

#### 2. .kiro Directory Structure
```
.kiro/
├── steering/          # Development guidelines (REQUIRED)
│   ├── project-context.md
│   ├── python-standards.md
│   ├── api-development.md
│   ├── image-generation.md
│   ├── docker-deployment.md
│   ├── testing-strategy.md
│   └── configuration-management.md
├── hooks/            # Agent hooks for automation (REQUIRED)
│   └── [hook files]
└── specs/            # Feature specifications (OPTIONAL but recommended)
    └── [spec directories]
```

**CRITICAL**: Do NOT add .kiro directory to .gitignore!

#### 3. Demonstration Video
- Maximum 3 minutes length
- Show project functioning on target device
- Upload to YouTube, Vimeo, Facebook Video, or Youku
- Include link in submission form
- No copyrighted music or third-party trademarks

#### 4. Text Description
- Explain features and functionality
- Describe how Kiro was used in development
- Highlight innovative aspects
- Explain category fit

#### 5. Kiro Usage Documentation
Must demonstrate effective use of Kiro features:

**Vibe Coding**:
- How conversations with Kiro structured the project
- Most impressive code generation examples
- Development workflow with Kiro

**Agent Hooks**:
- Specific workflows automated
- How hooks improved development process
- Examples of hook configurations

**Spec-driven Development**:
- How specs structured implementation
- Comparison to vibe coding approach
- Benefits of spec-driven workflow

**Steering Docs**:
- How steering improved Kiro's responses
- Strategies that made biggest difference
- Examples of effective steering

**MCP** (if applicable):
- How extending Kiro's capabilities helped
- Features enabled by MCP
- Workflow improvements

## Judging Criteria

### Equally Weighted Criteria

#### 1. Potential Value (33%)
- **Uniqueness**: How saturated is the market?
- **Usability**: Is the UI intuitive?
- **Scalability**: Clear need and extensibility?

**SumiClock Strengths**:
- Unique niche: E-paper clock displays
- Simple, intuitive single-endpoint API
- Extensible: timezone support, caching, Docker deployment
- Clear need: Low-power always-on displays

#### 2. Implementation (33%)
- **Kiro Usage**: How effectively was Kiro used?
- **Feature Variety**: Multiple Kiro capabilities used?
- **Understanding Depth**: Deep understanding of features?
- **Experimentation**: Strategic decisions in workflow?

**SumiClock Approach**:
- Steering docs for development standards
- Agent hooks for workflow automation
- Specs for feature development
- MCP integration (optional)

#### 3. Quality and Design (33%)
- **Creativity**: Unique approach or resources?
- **Originality**: Novel solution to challenge?
- **Polish**: Thoughtful UI/UX choices?

**SumiClock Strengths**:
- Minimalist, elegant design
- E-paper optimization (high contrast)
- Clean architecture
- Well-documented codebase

## Development Strategy with Kiro

### Phase 1: Steering Documentation (COMPLETED)
- ✅ Project context and overview
- ✅ Python development standards
- ✅ API development guidelines
- ✅ Image generation best practices
- ✅ Docker deployment guide
- ✅ Testing strategy
- ✅ Configuration management

### Phase 2: Agent Hooks (NEXT)
Create hooks for:
- **Test automation**: Run tests on file save
- **Image validation**: Verify generated images
- **Linting**: Auto-format code on save
- **Documentation**: Update docs on code changes

### Phase 3: Spec-driven Development (RECOMMENDED)
Create specs for new features:
- Date display alongside time
- Weather information integration
- Multiple timezone support
- Custom themes and layouts
- Battery-friendly update intervals

### Phase 4: MCP Integration (OPTIONAL)
Potential MCP servers:
- Weather API integration
- Timezone database queries
- Image optimization tools
- E-paper device testing

## Submission Checklist

### Pre-Submission
- [ ] Code is clean and well-documented
- [ ] All tests passing
- [ ] README is comprehensive
- [ ] .kiro directory is complete and NOT in .gitignore
- [ ] License file is present and visible
- [ ] Repository is public

### Submission Materials
- [ ] Repository URL ready
- [ ] Demonstration video uploaded and public
- [ ] Text description written
- [ ] Kiro usage documentation prepared
- [ ] Category selected (Resurrection or Costume Contest)
- [ ] Screenshots/images prepared

### Kiro Documentation
- [ ] Steering docs usage explained
- [ ] Agent hooks demonstrated
- [ ] Spec-driven development shown (if applicable)
- [ ] Development workflow documented
- [ ] Before/after comparisons (if applicable)

## Presentation Tips

### Video Content
1. **Introduction** (30 seconds)
   - What is SumiClock?
   - Problem it solves
   - Target devices (Kindle, Kobo)

2. **Demo** (90 seconds)
   - Show clock on actual E-paper device
   - Demonstrate timezone changes
   - Show caching performance
   - Display configuration options

3. **Technical Highlights** (60 seconds)
   - Docker deployment
   - Redis caching
   - E-paper optimization
   - Kiro development workflow

### Text Description Structure
1. **Overview**: What and why
2. **Features**: Key functionality
3. **Technology**: Stack and architecture
4. **Kiro Usage**: How Kiro accelerated development
5. **Category Fit**: Why Resurrection/Costume Contest
6. **Future Plans**: Potential enhancements

## Resurrection Category Justification

### "Dead" Technology: E-Paper Displays
- Kindle/Kobo browsers are limited and rarely used
- E-paper displays seen as "old tech"
- Limited developer interest in E-ink applications

### Bringing It Back to Life
- Modern web APIs (FastAPI, Redis)
- Docker containerization
- Cloud deployment ready
- Timezone-aware, globally useful
- Extensible architecture for future features

### Solving Tomorrow's Problems
- Low-power always-on displays
- Sustainable computing
- Reduced energy consumption
- Ambient information displays
- IoT integration potential

## Tips for Success

### Maximize Kiro Impact
- Document every Kiro interaction
- Show before/after code examples
- Explain decision-making process
- Demonstrate workflow improvements
- Highlight time savings

### Polish the Submission
- Professional video quality
- Clear audio narration
- Smooth demo flow
- Comprehensive documentation
- Clean, readable code

### Stand Out
- Unique use case (E-paper displays)
- Clean, minimalist design
- Well-architected codebase
- Comprehensive Kiro usage
- Clear category fit

## Post-Submission

### After Submitting
- Share on social media (#hookedonkiro, @kirodotdev)
- Write blog post on dev.to/kirodotdev
- Engage with community
- Continue development
- Prepare for judging questions

### Bonus Prizes
- **Social Blitz**: Post about Kiro on social media
- **Blog Post**: Write about development experience
- **Startup Project**: If applicable, highlight startup potential
