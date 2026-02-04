---
name: nestjs-conventions
description: Park Golf Platform NestJS 코딩 컨벤션. 모듈 구조, 서비스/컨트롤러 작성 규칙, DTO/Entity 패턴, 의존성 주입 방법 안내. "NestJS", "컨벤션", "코딩 스타일", "모듈", "서비스" 관련 질문 시 사용합니다.
---

# NestJS 코딩 컨벤션

## 1. 프로젝트 구조

### 1.1 서비스별 구조 (Backend Services)

```
services/{service-name}/
├── src/
│   ├── {domain}/                    # 도메인별 폴더 (예: game, booking)
│   │   ├── controller/              # NATS 컨트롤러 (마이크로서비스)
│   │   │   └── {domain}-nats.controller.ts
│   │   ├── service/                 # 비즈니스 로직
│   │   │   └── {domain}.service.ts
│   │   ├── dto/                     # Data Transfer Objects
│   │   │   └── {domain}.dto.ts
│   │   └── {domain}.module.ts       # 모듈 정의
│   │
│   ├── common/                      # 공통 유틸리티
│   │   ├── utils/
│   │   │   └── response.util.ts     # 표준 응답 포맷
│   │   └── filters/
│   │       └── exception.filter.ts
│   │
│   ├── prisma/                      # Prisma 설정
│   │   ├── prisma.module.ts
│   │   ├── prisma.service.ts
│   │   └── schema.prisma
│   │
│   ├── app.module.ts
│   └── main.ts
│
├── Dockerfile
├── package.json
└── tsconfig.json
```

### 1.2 BFF 서비스 구조 (admin-api, user-api)

```
services/{bff-api}/
├── src/
│   ├── {domain}/                    # 도메인별 폴더
│   │   ├── {domain}.controller.ts   # REST 컨트롤러
│   │   ├── {domain}.service.ts      # NATS 클라이언트 래퍼
│   │   ├── {domain}.module.ts
│   │   └── dto/
│   │       └── {domain}.dto.ts
│   │
│   ├── common/
│   │   └── nats/
│   │       ├── nats-client.module.ts
│   │       └── nats-client.service.ts
│   │
│   ├── auth/                        # 인증/인가
│   │   ├── guards/
│   │   │   └── jwt-auth.guard.ts
│   │   └── decorators/
│   │       └── current-user.decorator.ts
│   │
│   ├── app.module.ts
│   └── main.ts
```

---

## 2. 파일 명명 규칙

### 2.1 파일명 패턴

| 유형 | 패턴 | 예시 |
|------|------|------|
| 모듈 | `{name}.module.ts` | `game.module.ts` |
| 서비스 | `{name}.service.ts` | `game.service.ts` |
| REST 컨트롤러 | `{name}.controller.ts` | `game.controller.ts` |
| NATS 컨트롤러 | `{name}-nats.controller.ts` | `game-nats.controller.ts` |
| DTO | `{name}.dto.ts` | `game.dto.ts` |
| Entity (Prisma) | `schema.prisma` 내 정의 | - |
| Guard | `{name}.guard.ts` | `jwt-auth.guard.ts` |
| Filter | `{name}.filter.ts` | `http-exception.filter.ts` |
| Decorator | `{name}.decorator.ts` | `current-user.decorator.ts` |

### 2.2 클래스 명명 규칙

```typescript
// 모듈
export class GameModule {}

// 서비스
@Injectable()
export class GameService {}

// REST 컨트롤러
@Controller('api/admin/games')
export class GameController {}

// NATS 컨트롤러
@Controller()
export class GameNatsController {}

// DTO
export class CreateGameDto {}
export class UpdateGameDto {}
export class GameResponseDto {}

// Guard
@Injectable()
export class JwtAuthGuard implements CanActivate {}
```

---

## 3. 모듈 구성

### 3.1 Feature 모듈 템플릿

```typescript
// game.module.ts
import { Module } from '@nestjs/common';
import { GameService } from './service/game.service';
import { GameNatsController } from './controller/game-nats.controller';

@Module({
  controllers: [GameNatsController],
  providers: [GameService],
  exports: [GameService],  // 다른 모듈에서 사용 시
})
export class GameModule {}
```

### 3.2 App 모듈 (마이크로서비스)

```typescript
// app.module.ts (Backend Service)
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { PrismaModule } from './prisma/prisma.module';
import { GameModule } from './game/game.module';
import { BookingModule } from './booking/booking.module';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule,
    GameModule,
    BookingModule,
  ],
})
export class AppModule {}
```

---

## 4. 서비스 작성 규칙

### 4.1 서비스 클래스 구조

```typescript
// game.service.ts
import { Injectable, Logger, NotFoundException } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';
import { CreateGameDto, UpdateGameDto } from '../dto/game.dto';

@Injectable()
export class GameService {
  private readonly logger = new Logger(GameService.name);

  constructor(private readonly prisma: PrismaService) {}

  // ============================================
  // CREATE
  // ============================================
  async create(dto: CreateGameDto) {
    this.logger.log(`Creating game: ${dto.name}`);

    return this.prisma.game.create({
      data: {
        name: dto.name,
        code: dto.code,
        // ... 기타 필드
      },
      include: {
        frontNineCourse: true,
        backNineCourse: true,
      },
    });
  }

  // ============================================
  // READ
  // ============================================
  async findAll(query: any) {
    const { page = 1, limit = 20, clubId } = query;
    const skip = (page - 1) * limit;

    const where = clubId ? { clubId } : {};

    const [data, total] = await this.prisma.$transaction([
      this.prisma.game.findMany({ where, skip, take: limit }),
      this.prisma.game.count({ where }),
    ]);

    return { data, total, page, limit };
  }

  async findById(id: number) {
    const game = await this.prisma.game.findUnique({
      where: { id },
      include: { frontNineCourse: true, backNineCourse: true },
    });

    if (!game) {
      throw new NotFoundException(`Game with ID ${id} not found`);
    }

    return game;
  }

  // ============================================
  // UPDATE
  // ============================================
  async update(id: number, dto: UpdateGameDto) {
    await this.findById(id);  // 존재 확인

    return this.prisma.game.update({
      where: { id },
      data: dto,
    });
  }

  // ============================================
  // DELETE
  // ============================================
  async remove(id: number) {
    await this.findById(id);

    return this.prisma.game.delete({ where: { id } });
  }
}
```

### 4.2 주석 섹션 규칙

```typescript
// 기능별로 섹션 구분
// ============================================
// Game Management
// ============================================

// ============================================
// Weekly Schedule Management
// ============================================

// ============================================
// Time Slot Management
// ============================================
```

---

## 5. 컨트롤러 작성 규칙

### 5.1 NATS 컨트롤러 (마이크로서비스)

```typescript
// game-nats.controller.ts
import { Controller, Logger } from '@nestjs/common';
import { MessagePattern, Payload } from '@nestjs/microservices';
import { GameService } from '../service/game.service';
import { successResponse, errorResponse } from '../../common/utils/response.util';

@Controller()
export class GameNatsController {
  private readonly logger = new Logger(GameNatsController.name);

  constructor(private readonly gameService: GameService) {}

  @MessagePattern('games.list')
  async listGames(@Payload() payload: any) {
    try {
      this.logger.log('NATS: Received games.list request');
      const result = await this.gameService.findAll(payload);
      return successResponse(result);
    } catch (error) {
      this.logger.error(`NATS: Error listing games: ${error.message}`);
      return errorResponse('GAME_LIST_FAILED', error.message);
    }
  }

  @MessagePattern('games.create')
  async createGame(@Payload() payload: any) {
    try {
      // BFF에서 { data, token } 형태로 전송
      const data = payload.data || payload;
      this.logger.log(`NATS: Creating game: ${data.name}`);

      const game = await this.gameService.create(data);
      return successResponse(game);
    } catch (error) {
      this.logger.error(`NATS: Error creating game: ${error.message}`);
      return errorResponse('GAME_CREATE_FAILED', error.message);
    }
  }
}
```

### 5.2 REST 컨트롤러 (BFF)

```typescript
// game.controller.ts (admin-api)
import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Body,
  Param,
  Query,
  UseGuards,
  Request,
  Logger,
} from '@nestjs/common';
import {
  ApiTags,
  ApiOperation,
  ApiResponse,
  ApiBearerAuth,
} from '@nestjs/swagger';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { GameService } from './game.service';
import { CreateGameDto, UpdateGameDto } from './dto/game.dto';

@ApiTags('Games')
@Controller('api/admin/games')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class GameController {
  private readonly logger = new Logger(GameController.name);

  constructor(private readonly gameService: GameService) {}

  @Get()
  @ApiOperation({ summary: '게임 목록 조회' })
  @ApiResponse({ status: 200, description: '성공' })
  async findAll(@Query() query: any, @Request() req: any) {
    return this.gameService.getGames(query, req.user.token);
  }

  @Get(':id')
  @ApiOperation({ summary: '게임 상세 조회' })
  async findOne(@Param('id') id: number, @Request() req: any) {
    return this.gameService.getGameById(id, req.user.token);
  }

  @Post()
  @ApiOperation({ summary: '게임 생성' })
  @ApiResponse({ status: 201, description: '생성됨' })
  async create(@Body() dto: CreateGameDto, @Request() req: any) {
    return this.gameService.createGame(dto, req.user.token);
  }

  @Put(':id')
  @ApiOperation({ summary: '게임 수정' })
  async update(
    @Param('id') id: number,
    @Body() dto: UpdateGameDto,
    @Request() req: any,
  ) {
    return this.gameService.updateGame(id, dto, req.user.token);
  }

  @Delete(':id')
  @ApiOperation({ summary: '게임 삭제' })
  async remove(@Param('id') id: number, @Request() req: any) {
    return this.gameService.deleteGame(id, req.user.token);
  }
}
```

---

## 6. DTO 작성 규칙

### 6.1 DTO 구조

```typescript
// game.dto.ts
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';
import {
  IsString,
  IsNumber,
  IsBoolean,
  IsOptional,
  IsNotEmpty,
  Min,
  Max,
} from 'class-validator';
import { Type } from 'class-transformer';

// ============================================
// Create DTO
// ============================================
export class CreateGameDto {
  @ApiProperty({ description: '게임명', example: 'A+B 코스' })
  @IsString()
  @IsNotEmpty()
  name: string;

  @ApiProperty({ description: '게임 코드', example: 'G-001' })
  @IsString()
  @IsNotEmpty()
  code: string;

  @ApiPropertyOptional({ description: '설명' })
  @IsString()
  @IsOptional()
  description?: string;

  @ApiProperty({ description: '전반 9홀 코스 ID', example: 1 })
  @IsNumber()
  @Type(() => Number)
  frontNineCourseId: number;

  @ApiProperty({ description: '후반 9홀 코스 ID', example: 2 })
  @IsNumber()
  @Type(() => Number)
  backNineCourseId: number;

  @ApiPropertyOptional({ description: '최대 플레이어 수', example: 4 })
  @IsNumber()
  @IsOptional()
  @Min(1)
  @Max(8)
  @Type(() => Number)
  maxPlayers?: number;

  @ApiProperty({ description: '기본 가격', example: 30000 })
  @IsNumber()
  @Min(0)
  @Type(() => Number)
  basePrice: number;

  @ApiPropertyOptional({ description: '활성 여부', default: true })
  @IsBoolean()
  @IsOptional()
  isActive?: boolean;
}

// ============================================
// Update DTO (모든 필드 Optional)
// ============================================
export class UpdateGameDto {
  @ApiPropertyOptional({ description: '게임명' })
  @IsString()
  @IsOptional()
  name?: string;

  @ApiPropertyOptional({ description: '설명' })
  @IsString()
  @IsOptional()
  description?: string;

  @ApiPropertyOptional({ description: '기본 가격' })
  @IsNumber()
  @IsOptional()
  @Min(0)
  @Type(() => Number)
  basePrice?: number;

  @ApiPropertyOptional({ description: '활성 여부' })
  @IsBoolean()
  @IsOptional()
  isActive?: boolean;
}

// ============================================
// Query DTO (목록 조회용)
// ============================================
export class GameQueryDto {
  @ApiPropertyOptional({ description: '페이지', default: 1 })
  @IsNumber()
  @IsOptional()
  @Min(1)
  @Type(() => Number)
  page?: number;

  @ApiPropertyOptional({ description: '페이지 크기', default: 20 })
  @IsNumber()
  @IsOptional()
  @Min(1)
  @Max(100)
  @Type(() => Number)
  limit?: number;

  @ApiPropertyOptional({ description: '클럽 ID 필터' })
  @IsNumber()
  @IsOptional()
  @Type(() => Number)
  clubId?: number;

  @ApiPropertyOptional({ description: '활성 상태 필터' })
  @IsBoolean()
  @IsOptional()
  @Type(() => Boolean)
  isActive?: boolean;
}

// ============================================
// Response DTO
// ============================================
export class GameResponseDto {
  @ApiProperty()
  id: number;

  @ApiProperty()
  name: string;

  @ApiProperty()
  code: string;

  @ApiProperty()
  description: string;

  @ApiProperty()
  frontNineCourseId: number;

  @ApiProperty()
  frontNineCourseName: string;

  @ApiProperty()
  backNineCourseId: number;

  @ApiProperty()
  backNineCourseName: string;

  @ApiProperty()
  totalHoles: number;

  @ApiProperty()
  maxPlayers: number;

  @ApiProperty()
  basePrice: number;

  @ApiProperty()
  isActive: boolean;

  @ApiProperty()
  createdAt: Date;

  @ApiProperty()
  updatedAt: Date;
}
```

---

## 7. 표준 응답 포맷

### 7.1 Response Utility

```typescript
// common/utils/response.util.ts

// 성공 응답
export function successResponse<T>(data: T, meta?: any) {
  return {
    success: true,
    data,
    ...(meta && { meta }),
  };
}

// 에러 응답
export function errorResponse(code: string, message: string) {
  return {
    success: false,
    error: {
      code,
      message,
    },
  };
}

// 페이지네이션 메타
export function paginationMeta(total: number, page: number, limit: number) {
  return {
    total,
    page,
    limit,
    totalPages: Math.ceil(total / limit),
  };
}
```

### 7.2 응답 형태

```json
// 성공 (단일)
{
  "success": true,
  "data": { "id": 1, "name": "A+B 코스" }
}

// 성공 (목록)
{
  "success": true,
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "totalPages": 5
  }
}

// 에러
{
  "success": false,
  "error": {
    "code": "GAME_NOT_FOUND",
    "message": "Game with ID 999 not found"
  }
}
```

---

## 8. NATS 메시지 패턴 규칙

### 8.1 패턴 명명

```
{도메인}.{동작}

예시:
- games.list
- games.findById
- games.create
- games.update
- games.delete

- gameTimeSlots.list
- gameTimeSlots.generate
- gameTimeSlots.getByGameAndDate

- gameWeeklySchedules.create
- gameWeeklySchedules.getByGame
```

### 8.2 페이로드 구조 (BFF → Service)

```typescript
// BFF에서 전송
{
  data: { ...실제데이터 },
  token: "jwt-token"  // 필요시
}

// Service에서 수신
@MessagePattern('games.create')
async createGame(@Payload() payload: any) {
  const data = payload.data || payload;  // 호환성
  // ...
}
```

---

## 9. 의존성 주입 규칙

### 9.1 생성자 주입 (권장)

```typescript
@Injectable()
export class GameService {
  constructor(
    private readonly prisma: PrismaService,
    private readonly natsClient: NatsClientService,  // 필요시
    @Inject('BOOKING_SERVICE') private readonly bookingClient: ClientProxy,  // 선택적
  ) {}
}
```

### 9.2 Optional 의존성

```typescript
@Injectable()
export class BookingService {
  constructor(
    private readonly prisma: PrismaService,
    @Optional() @Inject('NOTIFICATION_SERVICE')
    private readonly notificationClient?: ClientProxy,
  ) {}

  async create(dto: CreateBookingDto) {
    const booking = await this.prisma.booking.create({ data: dto });

    // Optional 서비스 사용
    if (this.notificationClient) {
      this.notificationClient.emit('booking.confirmed', booking);
    }

    return booking;
  }
}
```

---

## 10. 로깅 규칙

```typescript
@Injectable()
export class GameService {
  private readonly logger = new Logger(GameService.name);

  async create(dto: CreateGameDto) {
    this.logger.log(`Creating game: ${dto.name}`);

    try {
      const result = await this.prisma.game.create({ data: dto });
      this.logger.log(`Game created with ID: ${result.id}`);
      return result;
    } catch (error) {
      this.logger.error(`Failed to create game: ${error.message}`, error.stack);
      throw error;
    }
  }
}

// NATS 컨트롤러에서
@MessagePattern('games.create')
async createGame(@Payload() payload: any) {
  this.logger.log(`NATS: Received games.create request`);
  this.logger.debug(`NATS: Payload: ${JSON.stringify(payload)}`);
  // ...
}
```
