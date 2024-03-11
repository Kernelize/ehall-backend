pub mod nnu;
pub mod nuaa;
pub mod ysu;

use crate::models::user::{CourseTable, ExamSchedule, Info, LoginType, Notification, Score};
use async_trait::async_trait;
use axum::{body::Body, extract::Request, response::Response};
use futures::future::BoxFuture;
use std::{
    future::Future,
    pin::Pin,
    task::{Context, Poll},
};
use tower::{BoxError, Service};

#[async_trait]
pub trait SchoolAdapter {
    async fn login(&self, login: &LoginType) -> Result<(), String>;

    async fn fetch_user_info(&self) -> Result<Info, String>;

    async fn fetch_scores(&self) -> Result<Vec<Score>, String> {
        unimplemented!()
    }

    async fn fetch_course_table(&self) -> Result<Vec<CourseTable>, String> {
        unimplemented!()
    }

    async fn fetch_exam_schedule(&self) -> Result<ExamSchedule, String> {
        unimplemented!()
    }

    async fn fetch_notifications(&self) -> Result<Vec<Notification>, String> {
        unimplemented!()
    }
}

struct SchoolService<T: SchoolAdapter> {
    adapter: T,
}

impl<T, B> Service<Request<B>> for SchoolService<T>
where
    T: SchoolAdapter + Clone + Send + 'static,
    B: Send + 'static,
{
    type Response = Response;
    type Error = String;
    type Future = BoxFuture<'static, Result<Self::Response, Self::Error>>;

    fn poll_ready(&mut self, _cx: &mut Context<'_>) -> Poll<Result<(), Self::Error>> {
        Poll::Ready(Ok(()))
    }

    fn call(&mut self, request: Request<B>) -> Self::Future {
        let adapter = self.adapter.clone();
        let response = async move {
            // Some shits

            Ok(Response::new(Body::from("Hello from SchoolAdapter")))
        };
        Box::pin(response)
    }
}
